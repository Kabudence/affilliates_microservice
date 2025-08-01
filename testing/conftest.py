"""
Conftest para ejecutar los tests en la BD real de Flask.
NO se toca el schema; todo va dentro de una transacción que
se revierte al terminar cada test.
"""
import pytest

from rental.application.commands.user_goal_command_service import UserGoalCommandService
from rental.application.queries.goal_query_service import GoalQueryService
from rental.infraestructure.Repositories.user_goal_repository import UserGoalRepository
# ------------- importa el objeto db que ya usa tu app -------------
from shared.infrastructure.database import db as real_db

# ---- importa TODOS los modelos una sola vez (usan el mismo db) ----
from application.infraestructure.model.application_data_model import ApplicationModel
from rental.infraestructure.model.module_model import ModuleModel
from rental.infraestructure.model.plan_model import PlanModel, PlanModuleModel
from rental.infraestructure.model.goal_model import GoalModel
from users.infraestructure.models.user_model import UserModel
from rental.infraestructure.model.subscription_model import SubscriptionModel
from rental.infraestructure.model.commissions_model import CommissionModel
# … añade cualquier otro modelo si lo necesitas …

# ------------------------------------------------------------------
# 1) Conectamos a la BD REAL una sola vez por sesión de test
# ------------------------------------------------------------------
@pytest.fixture(scope="session", autouse=True)
def _connect_real_db():
    if real_db.is_closed():
        real_db.connect(reuse_if_open=True)
    yield
    real_db.close()

# ------------------------------------------------------------------
# 2) Iniciamos transacción por test y hacemos ROLLBACK al final
# ------------------------------------------------------------------
@pytest.fixture(scope="function", autouse=True)
def db_transaction():
    """
    Todo lo que se inserte/actualice dentro del test
    se revierte con rollback --> la BD queda limpia.
    """
    with real_db.atomic() as tx:
        yield
        tx.rollback()

# ------------------------------------------------------------------
# 3) Aquí abajo inyectas tus repos y services REALES
#    (¡ya usan el mismo db, no hay que cambiarlos!)
# ------------------------------------------------------------------
from application.application.command.application_command_service import ApplicationCommandService
from rental.application.commands.module_command_service import ModuleCommandService
from rental.application.commands.plan_command_service import PlanCommandService
from rental.application.commands.goal_command_service import GoalCommandService
from rental.application.commands.subscription_command_service import SubscriptionCommandService
from rental.application.commands.commissions_command_service import CommissionCommandService
from users.application.command.user_command_service import UserCommandService
from users.application.query.user_query_service import UserQueryService
from rental.application.user_flow_service import UserFlowService

from application.infraestructure.repositories.application_data_repository import ApplicationRepository
from rental.infraestructure.Repositories.module_repository import ModuleRepository
from rental.infraestructure.Repositories.plan_repository import PlanRepository
from rental.infraestructure.Repositories.module_plan_repository import PlanModuleRepository
from rental.infraestructure.Repositories.goal_repository import GoalRepository
from rental.infraestructure.Repositories.subscription_repository import SubscriptionRepository
from rental.infraestructure.Repositories.commissions_repository import CommissionRepository
from users.infraestructure.repositories.user_repository import UserRepository

# ---- fixtures repos ----
@pytest.fixture      ()
def application_repo():  return ApplicationRepository()
@pytest.fixture      ()
def module_repo():       return ModuleRepository()
@pytest.fixture      ()
def plan_repo():         return PlanRepository()
@pytest.fixture      ()
def plan_module_repo():  return PlanModuleRepository()
@pytest.fixture      ()
def goal_repo():         return GoalRepository()
@pytest.fixture      ()
def subscription_repo(): return SubscriptionRepository()
@pytest.fixture      ()
def commission_repo():   return CommissionRepository()
@pytest.fixture      ()
def user_repo():         return UserRepository()

# ---- fixture repositorio de UserGoal real ----
@pytest.fixture()
def user_goal_repo():
    return UserGoalRepository()

# ------------------------------------------------------------------
# 4)  —  FACTORÍAS (services) REALES
# ------------------------------------------------------------------
@pytest.fixture()
def app_cmd(application_repo):
    return ApplicationCommandService(application_repo)

@pytest.fixture()
def module_cmd(module_repo):
    return ModuleCommandService(module_repo)

@pytest.fixture()
def plan_cmd(plan_repo, plan_module_repo):
    return PlanCommandService(plan_repo, plan_module_repo)

@pytest.fixture()
def goal_cmd(goal_repo):
    return GoalCommandService(goal_repo)

# ---------- Query-service de GOAL ----------------
@pytest.fixture()
def goal_query(goal_repo):
    return GoalQueryService(goal_repo)          # ⬅️  ❗ NUEVO

@pytest.fixture()
def subs_cmd(subscription_repo):
    return SubscriptionCommandService(subscription_repo)
# … parte que ya tienes arriba …

@pytest.fixture()
def comm_cmd(commission_repo):
    return CommissionCommandService(commission_repo)

# --------- resto de services estándar ----------
@pytest.fixture()
def user_cmd(user_repo):
    return UserCommandService(user_repo)

@pytest.fixture()
def user_query(user_repo):
    return UserQueryService(user_repo)

# ---------- User-Goal services -----------------
@pytest.fixture()
def user_goal_cmd(user_goal_repo):
    return UserGoalCommandService(user_goal_repo)

# ---------- User-Flow (service bajo prueba) ----
@pytest.fixture()
def user_flow(
        user_cmd,
        user_query,
        user_goal_cmd,
        subs_cmd,
        comm_cmd,
        plan_cmd,
        goal_query,      # ⬅️  se inyecta aquí
):
    return UserFlowService(
        user_goal_command_service=user_goal_cmd,
        user_command_service=user_cmd,
        user_query_service=user_query,
        subscription_command_service=subs_cmd,
        commission_command_service=comm_cmd,
        plan_query_service=plan_cmd,
        goal_query_service=goal_query,   # ⬅️  ¡ahora sí lo recibe!
    )
