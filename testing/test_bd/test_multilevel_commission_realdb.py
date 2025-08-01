# testing/test_multilevel_commission_realdb.py
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
# Test: afiliado padre  ➜  afiliado hijo  ➜  buyers  ----------------
# ------------------------------------------------------------------
def test_multilevel_commission_flow(
    app_cmd,
    module_cmd,
    plan_cmd,
    goal_cmd,
    user_cmd,
    user_flow,
    commission_repo,      # ⬅️ para consultar importes al final
):
    log = logging.getLogger("FLOW")

    # 1) APP --------------------------------------------------------
    app = app_cmd.create(
        name="APP-" + uuid.uuid4().hex[:6],
        description="App multilevel test",
        application_type=ApplicationType.EMPRENDEX,
    )

    # 2) Módulos ----------------------------------------------------
    modules = [
        module_cmd.create(name=f"Modulo {i}", description=f"Descripción módulo {i}") for i in range(1, 4)
    ]

    # 3) Plan -------------------------------------------------------
    plan = plan_cmd.create(
        name="Plan Platinum",
        description="Plan de prueba",
        duration=30,
        price=100.0,
        app_id=app.id,
        ids_modules=[m.id for m in modules],
    )

    # 4) Meta de 7 clientes ----------------------------------------
    goal_cmd.create(number_of_clients=7, month=1, percentage_to_bonus=0.10)

    # 5) Mock de API externa ---------------------------------------
    external_counter = 0

    def fake_create_emprede_user(*_, **__):
        nonlocal external_counter
        external_counter += 1
        return 201, {"id": 20_000 + external_counter}

    api_path = (
        "users.infraestructure.external_users_api."
        "external_user_api.create_emprede_user"
    )

    buyers_per_affiliate = 10

    with patch(api_path, side_effect=fake_create_emprede_user):

        # ▸▸  Padre afiliado
        _, body = fake_create_emprede_user()
        parent_aff = user_cmd.create(
            account_id=body["id"],
            app_id=app.id,
            user_type=UserType.AFILIATE,
        )
        user_flow.user_flow(parent_aff.id)    # crea UserGoal

        # ▸▸  Hijo afiliado (owner = padre)
        _, body = fake_create_emprede_user()
        child_aff = user_cmd.create(
            account_id=body["id"],
            app_id=app.id,
            user_type=UserType.AFILIATE,
            user_owner_id=parent_aff.id,
        )
        user_flow.user_flow(child_aff.id)     # crea UserGoal

        # ▸▸  10 buyers para el PADRE
        for _ in range(buyers_per_affiliate):
            _, body = fake_create_emprede_user()
            buyer = user_cmd.create(
                account_id=body["id"],
                app_id=app.id,
                user_type=UserType.BUYER,
                user_owner_id=parent_aff.id,
            )
            user_flow.user_flow(buyer.id, plan.id)

        # ▸▸  10 buyers para el HIJO
        for _ in range(buyers_per_affiliate):
            _, body = fake_create_emprede_user()
            buyer = user_cmd.create(
                account_id=body["id"],
                app_id=app.id,
                user_type=UserType.BUYER,
                user_owner_id=child_aff.id,
            )
            user_flow.user_flow(buyer.id, plan.id)

    # 6) Totales de comisiones -------------------------------------
    parent_comm = commission_repo.get_all_by_user_id(parent_aff.id)
    child_comm  = commission_repo.get_all_by_user_id(child_aff.id)

    total_parent = sum(c.amount for c in parent_comm)
    total_child  = sum(c.amount for c in child_comm)

    log.info("💰 Total padre  : %.2f (comisiones=%s)", total_parent, len(parent_comm))
    log.info("💰 Total hijo   : %.2f (comisiones=%s)", total_child,  len(child_comm))

    # 7) Asserts ----------------------------------------------------
    # 7.1 ambos afiliados deben tener 10 buyers directos
    for aff in (parent_aff, child_aff):
        buyers = [
            u for u in user_cmd.user_repo.get_all()
            if u.user_type == UserType.BUYER and u.user_owner_id == aff.id
        ]
        assert len(buyers) == buyers_per_affiliate

    # 7.2 las metas de 7 clientes deben estar cumplidas en ambos
    for aff in (parent_aff, child_aff):
        ug = user_flow.user_goal_command_service.list_by_user(aff.id)[0]
        assert ug.goal_attained

    # 7.3 el padre debe ganar MÁS que el hijo
    assert total_parent > total_child, (
        f"Se esperaba total padre > hijo (padre={total_parent}, hijo={total_child})"
    )

    log.info("✅ Flujo multilevel finalizado sin errores")
