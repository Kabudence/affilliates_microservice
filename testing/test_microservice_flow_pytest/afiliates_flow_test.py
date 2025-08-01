import logging
from unittest.mock import patch

import pytest

from application.domain.entities.application_data import ApplicationType
from users.domain.model.entities.user import UserType


# ---------- Logging global ----------
@pytest.fixture(autouse=True, scope="session")
def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s [%(name)s] %(message)s",
    )


# ------------ TEST FLOW -------------
def test_full_affiliate_buyer_flow(
    app_command_service,
    module_cmd,
    plan_cmd,
    goal_cmd,
    user_cmd,
    user_flow,
):
    logger = logging.getLogger("test_flow")

    # 1. Crear APP
    app = app_command_service.create(
        name="InnovaApp",
        description="App de Demo para flow",
        application_type=ApplicationType.EMPRENDEX,
    )
    logger.info("APP creada: %s", app.id)

    # 2. Crear módulos
    modules = [
        module_cmd.create(name=f"Modulo{i}", description=f"Descripción módulo {i}")
        for i in range(1, 4)
    ]
    for m in modules:
        logger.info("Módulo creado (id=%s)", m.id)

    # 3. Crear plan
    plan = plan_cmd.create(
        name="Plan Gold",
        description="Plan de prueba",
        duration=30,
        price=100.0,
        app_id=app.id,
        ids_modules=[m.id for m in modules],
    )
    assert plan.id is not None
    logger.info("Plan creado (id=%s)", plan.id)

    # 4. Goals (7, 10, 15 clientes)
    for n in (7, 10, 15):
        g = goal_cmd.create(
            number_of_clients=n,
            month=1,
            percentage_to_bonus=0.10,
        )
        logger.info("Goal %s creado (%s clientes)", g.id, g.number_of_clients)

    # 5. Affiliates vía API externa mockeada
    external_counter = 0

    def fake_create_emprede_user(*_, **__):
        nonlocal external_counter
        external_counter += 1
        return 201, {"id": external_counter}

    with patch(
        "users.infraestructure.external_users_api.external_user_api.create_emprede_user",
        side_effect=fake_create_emprede_user,
    ):
        affiliates = []
        for _ in range(2):
            _, body = fake_create_emprede_user()
            aff = user_cmd.create(
                account_id=body["id"],
                app_id=app.id,
                user_type=UserType.AFILIATE,
            )
            user_flow.user_flow(aff.id)  # crea UserGoal inicial
            affiliates.append(aff)
            logger.info("Affiliate %s creado", aff.id)

    # 6. Buyers (20; 10 por affiliate)
    buyers_per_aff = 10
    for aff in affiliates:
        for _ in range(buyers_per_aff):
            external_counter += 1
            buyer = user_cmd.create(
                account_id=external_counter,
                app_id=app.id,
                user_type=UserType.BUYER,
                user_owner_id=aff.id,
            )
            user_flow.user_flow(buyer.id, plan.id)
            logger.info("Buyer %s asignado a Affiliate %s", buyer.id, aff.id)

    # 7. Validar metas cumplidas
    for aff in affiliates:
        buyers = [
            u for u in user_cmd.user_repo.get_all()
            if u.user_owner_id == aff.id and u.user_type == UserType.BUYER
        ]
        assert len(buyers) == buyers_per_aff

        ug = user_flow.user_goal_command_service.list_by_user(aff.id)[0]
        assert ug.goal_attained, "La meta de 7 clientes debería cumplirse"
        logger.info("Affiliate %s cumplió meta %s ✅", aff.id, ug.goal_id)

    logger.info("Flujo completo ✅")
