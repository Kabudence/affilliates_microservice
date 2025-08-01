# testing/test_only_level_comission.py
import logging
import uuid
from unittest.mock import patch

import pytest

from application.domain.entities.application_data import ApplicationType
from users.domain.model.entities.user import UserType

# ------------------------------------------------------------------
# Configura logs legibles durante el test
# ------------------------------------------------------------------
@pytest.fixture(autouse=True, scope="session")
def _configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s | %(message)s",
    )

# ------------------------------------------------------------------
# Test de flujo completo contra la BD real (con rollback por test)
# ------------------------------------------------------------------
def test_full_affiliate_buyer_flow(
    app_cmd,
    module_cmd,
    plan_cmd,
    goal_cmd,
    user_cmd,
    user_flow,
):
    log = logging.getLogger("FLOW")

    # 1) APP --------------------------------------------------------
    app = app_cmd.create(
        name="APP-" + uuid.uuid4().hex[:6],
        description="Aplicación de pruebas",
        application_type=ApplicationType.EMPRENDEX,
    )
    log.info("App creada id=%s", app.id)

    # 2) Módulos ----------------------------------------------------
    modules = [
        module_cmd.create(
            name=f"Modulo {i}",
            description=f"Descripción módulo {i}",
        )
        for i in range(1, 4)
    ]
    log.info("Módulos creados ids=%s", [m.id for m in modules])

    # 3) Plan -------------------------------------------------------
    plan = plan_cmd.create(
        name="Plan Gold",
        description="Plan de prueba",
        duration=30,
        price=100.0,
        app_id=app.id,
        ids_modules=[m.id for m in modules],
    )
    log.info("Plan creado id=%s", plan.id)

    # 4) Goals ------------------------------------------------------
    goals = [
        goal_cmd.create(number_of_clients=n, month=1, percentage_to_bonus=0.10)
        for n in (7, 10, 15)
    ]
    log.info("Goals creados ids=%s", [g.id for g in goals])

    # 5) Mock de API externa para crear usuarios emprende -----------
    external_counter = 0

    def fake_create_emprede_user(*_, **__):
        nonlocal external_counter
        external_counter += 1
        return 201, {"id": 10_000 + external_counter}  # ids altos ficticios

    api_path = (
        "users.infraestructure.external_users_api."
        "external_user_api.create_emprede_user"
    )

    with patch(api_path, side_effect=fake_create_emprede_user):
        # 5a) dos afiliados ----------------------------------------
        affiliates = []
        for _ in range(2):
            _, body = fake_create_emprede_user()
            affiliate = user_cmd.create(
                account_id=body["id"],
                app_id=app.id,
                user_type=UserType.AFILIATE,
            )
            user_flow.user_flow(affiliate.id)  # genera la meta para el afiliado
            affiliates.append(affiliate)
            log.info("Affiliate creado id=%s ext_account=%s",
                     affiliate.id, body["id"])

        # 6) 20 compradores (10 cada afiliado) ---------------------
        buyers_per_affiliate = 10
        for idx, aff in enumerate(affiliates):
            for _ in range(buyers_per_affiliate):
                _, body = fake_create_emprede_user()
                buyer = user_cmd.create(
                    account_id=body["id"],
                    app_id=app.id,
                    user_type=UserType.BUYER,
                    user_owner_id=aff.id,
                )
                user_flow.user_flow(buyer.id, plan.id)
            log.info("Se crearon %s buyers para affiliate id=%s",
                     buyers_per_affiliate, aff.id)

    # 7) Validaciones ----------------------------------------------
    for aff in affiliates:
        # 7.1  ── Cada afiliado debe tener 10 buyers
        buyers = [
            u
            for u in user_cmd.user_repo.get_all()
            if getattr(u, "user_owner_id", None) == aff.id
            and u.user_type == UserType.BUYER
        ]
        assert len(buyers) == buyers_per_affiliate, (
            f"Affiliate {aff.id} tiene {len(buyers)} buyers, "
            f"se esperaban {buyers_per_affiliate}"
        )

        # 7.2  ── Debe existir al menos un UserGoal
        ug_list = user_flow.user_goal_command_service.list_by_user(aff.id)
        assert ug_list, "Affiliate sin UserGoal asociado"

        # 7.3  ── La meta de 7 clientes debe estar cumplida
        assert ug_list[0].goal_attained, (
            f"Affiliate {aff.id} todavía no cumplió la meta de 7 clientes"
        )

    log.info("✅ Flujo completo sin errores")
