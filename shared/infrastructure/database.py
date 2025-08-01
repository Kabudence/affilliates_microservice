"""
Database connection + table-creation helpers.
¡¡NO IMPORTES modelos ARRIBA!!  Eso crea ciclos.
"""

from peewee import MySQLDatabase, SQL                    # SQL para constraints

from shared.infrastructure.db_config import DB_CONFIG

# ------------- conexión -------------
db = MySQLDatabase(**DB_CONFIG)

# Peewee expone peewee.SQL; algunos modelos usan db.SQL(…).
# Añadimos el alias para no tocar cada modelo.
if not hasattr(db, "SQL"):
    db.SQL = SQL


# ------------------------------------------------------------------
# Función para crear TODAS las tablas.  Importa modelos **dentro**.
# ------------------------------------------------------------------
def init_db() -> None:
    """
    Conecta (si está cerrada) y crea TODAS las tablas definidas en los modelos.
    Ejecuta con:  from shared.infrastructure.database import init_db; init_db()
    """
    if db.is_closed():
        db.connect(reuse_if_open=True)
        print("Driver conectado:", type(db._state.conn))

    # ------------ IMPORTS LOCALES ------------
    # Core-App
    from application.infraestructure.model.application_data_model import ApplicationModel
    from rental.infraestructure.model.module_model import ModuleModel
    from rental.infraestructure.model.plan_model import PlanModel, PlanModuleModel
    from rental.infraestructure.model.goal_model import GoalModel
    from users.infraestructure.models.user_model import UserModel
    from rental.infraestructure.model.user_goal_model import UserGoalModel

    # Socio-económico
    from socioeconomic_distribution.infraestructure.model.inscription_level_model import InscriptionLevelModel
    from socioeconomic_distribution.infraestructure.model.district_model import DistrictModel
    from socioeconomic_distribution.infraestructure.model.royalties_model import RoyaltiesModel

    # Rental / transacciones
    from rental.infraestructure.model.subscription_model import SubscriptionModel
    from rental.infraestructure.model.commissions_model import CommissionModel

    # ------------ CREAR TABLAS ---------------
    db.create_tables(
        [
            # Core
            ApplicationModel,
            ModuleModel,
            PlanModel,
            PlanModuleModel,
            GoalModel,
            UserModel,
            UserGoalModel,

            # Socio-económico
            InscriptionLevelModel,
            DistrictModel,
            RoyaltiesModel,

            # Transacciones
            SubscriptionModel,
            CommissionModel,
        ],
        safe=True,
    )

    print("✅ Tablas creadas/aseguradas.")
    db.close()
