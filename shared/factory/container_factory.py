# container.py
# ---------- IMPORTA TODOS TUS REPOSITORIOS ----------
from application.application.query.application_query_service import ApplicationQueryService
from application.infraestructure.repositories.application_data_repository import ApplicationRepository
from billing.application.command.card_command_service import CardCommandService
from billing.application.query.card_query_service import CardQueryService
from billing.infraestructure.repository.card_repository import CardRepository
from rental.application.commands.commissions_command_service import CommissionCommandService
from rental.application.commands.franchise_config_command_service import FranchiseConfigCommandService
from rental.application.commands.franchise_discount_command_service import FranchiseDiscountCommandService
from rental.application.commands.franchise_overpriced_command_service import FranchiseOverpricedCommandService
from rental.application.commands.goal_command_service import GoalCommandService
from rental.application.commands.module_command_service import ModuleCommandService
from rental.application.commands.percent_commissions_command_service import PercentCommissionCommandService
from rental.application.commands.plan_command_service import PlanCommandService
from rental.application.commands.plan_time_command_service import PlanTimeCommandService
from rental.application.commands.subscription_command_service import SubscriptionCommandService
from rental.application.commands.user_goal_command_service import UserGoalCommandService
from rental.application.queries.commissions_query_service import CommissionQueryService
from rental.application.queries.franchise_config_query_service import FranchiseConfigQueryService
from rental.application.queries.franchise_discount_query_service import FranchiseDiscountQueryService
from rental.application.queries.franchise_overpriced_query_service import FranchiseOverpricedQueryService
from rental.application.queries.goal_query_service import GoalQueryService
from rental.application.queries.module_query_service import ModuleQueryService
from rental.application.queries.percent_commissions_query_service import PercentCommissionQueryService
from rental.application.queries.plan_query_service import PlanQueryService
from rental.application.queries.plan_time_query_service import PlanTimeQueryService
from rental.application.queries.subscription_query_service import SubscriptionQueryService
from rental.application.user_flow_service import UserFlowService
from rental.infraestructure.Repositories.commissions_repository import CommissionRepository
from rental.infraestructure.Repositories.franchise_config_repository import FranchiseConfigRepository
from rental.infraestructure.Repositories.franchise_discount_repository import FranchiseDiscountRepository
from rental.infraestructure.Repositories.franchise_overpriced_repository import FranchiseOverpricedRepository
from rental.infraestructure.Repositories.goal_repository import GoalRepository
from rental.infraestructure.Repositories.module_repository import ModuleRepository
from rental.infraestructure.Repositories.percent_commission_repository import PercentCommissionRepository
from rental.infraestructure.Repositories.plan_repository import PlanRepository
from rental.infraestructure.Repositories.module_plan_repository import PlanModuleRepository
from rental.infraestructure.Repositories.plan_time_repository import PlanTimeRepository
from rental.infraestructure.Repositories.subscription_repository import SubscriptionRepository
from rental.infraestructure.Repositories.user_goal_repository import UserGoalRepository
from socioeconomic_distribution.application.command.district_command_service import DistrictCommandService
from socioeconomic_distribution.application.command.inscription_level_command_service import \
    InscriptionLevelCommandService
from socioeconomic_distribution.application.command.royalties_command_service import RoyaltiesCommandService
from socioeconomic_distribution.application.query.inscription_level_query_service import InscriptionLevelQueryService
from socioeconomic_distribution.application.query.royalties_query_service import RoyaltiesQueryService
from socioeconomic_distribution.infraestructure.repository.district_repository import DistrictRepository
from socioeconomic_distribution.infraestructure.repository.inscription_level_repository import InscriptionLevelRepository
from socioeconomic_distribution.infraestructure.repository.royalties_repository import RoyaltiesRepository
from users.application.command.user_command_service import UserCommandService
from users.application.query.user_query_service import UserQueryService
from users.infraestructure.repositories.user_repository import UserRepository

# ---------- IMPORTA TODOS TUS SERVICIOS ----------
from application.application.command.application_command_service import ApplicationCommandService


def build_services():
    # ---------- INSTANTIACIÓN DE REPOS ----------
    application_repo = ApplicationRepository()
    card_repo = CardRepository()
    commission_repo = CommissionRepository()
    goal_repo = GoalRepository()
    module_repo = ModuleRepository()
    plan_repo = PlanRepository()
    plan_module_repo = PlanModuleRepository()
    subscription_repo = SubscriptionRepository()
    user_goal_repo = UserGoalRepository()
    district_repo = DistrictRepository()
    inscription_level_repo = InscriptionLevelRepository()
    royalties_repo = RoyaltiesRepository()
    user_repo = UserRepository()
    plan_time_repo=PlanTimeRepository()
    percent_commission_repo = PercentCommissionRepository()
    franchise_discount_repo = FranchiseDiscountRepository()
    franchise_overpriced_repo = FranchiseOverpricedRepository()
    franchise_config_repo = FranchiseConfigRepository()
    # ---------- INSTANTIACIÓN DE SERVICES ----------
    # Application
    application_command_service = ApplicationCommandService(application_repo)
    application_query_service = ApplicationQueryService(application_repo)


    # Card
    card_command_service = CardCommandService(card_repo)
    card_query_service = CardQueryService(card_repo)

    # Commission
    commission_command_service = CommissionCommandService(commission_repo)
    commission_query_service = CommissionQueryService(commission_repo)

    # Goal
    goal_command_service = GoalCommandService(goal_repo)
    goal_query_service = GoalQueryService(goal_repo)

    # Module
    module_command_service = ModuleCommandService(module_repo)
    module_query_service = ModuleQueryService(module_repo)


    plan_time_command_service = PlanTimeCommandService(plan_time_repo)
    plan_time_query_service = PlanTimeQueryService(plan_time_repo)


    # Plan
    plan_command_service = PlanCommandService(plan_repo, plan_module_repo, plan_time_repo)
    plan_query_service = PlanQueryService(plan_repo)

    # Subscription
    subscription_command_service = SubscriptionCommandService(subscription_repo)
    subscription_query_service = SubscriptionQueryService(subscription_repo)
    # User Goal
    user_goal_command_service = UserGoalCommandService(user_goal_repo)

    # District
    district_command_service = DistrictCommandService(district_repo)

    # Inscription Level
    inscription_level_command_service = InscriptionLevelCommandService(inscription_level_repo)
    inscription_level_query_service = InscriptionLevelQueryService(inscription_level_repo)
    # Royalties
    royalties_command_service = RoyaltiesCommandService(royalties_repo)
    royalties_query_service = RoyaltiesQueryService(royalties_repo)
    # User
    user_command_service = UserCommandService(user_repo)
    user_query_service = UserQueryService(user_repo)

    # --- Percent Commission ---
    percent_commission_command_service = PercentCommissionCommandService(percent_commission_repo)
    percent_commission_query_service = PercentCommissionQueryService(percent_commission_repo)

    # --- Franchise Discount ---
    franchise_discount_command_service = FranchiseDiscountCommandService(franchise_discount_repo)
    franchise_discount_query_service = FranchiseDiscountQueryService(franchise_discount_repo)

    # --- Franchise Overpriced ---
    franchise_overpriced_command_service = FranchiseOverpricedCommandService(franchise_overpriced_repo)
    franchise_overpriced_query_service = FranchiseOverpricedQueryService(franchise_overpriced_repo)

    # --- Franchise Config ---
    franchise_config_command_service = FranchiseConfigCommandService(franchise_config_repo)
    franchise_config_query_service = FranchiseConfigQueryService(franchise_config_repo)


    user_flow_service = UserFlowService(
        user_goal_command_service=user_goal_command_service,
        user_command_service=user_command_service,
        user_query_service=user_query_service,
        subscription_command_service=subscription_command_service,
        commission_command_service=commission_command_service,
        plan_query_service=plan_query_service,
        goal_query_service=goal_query_service
    )

    return {
        # Application
        "application_command_service": application_command_service,
        "application_query_service": application_query_service,

        # Card
        "card_command_service": card_command_service,
        "card_query_service": card_query_service,

        # Commission
        "commission_command_service": commission_command_service,
        "commission_query_service": commission_query_service,
        # Goal
        "goal_command_service": goal_command_service,
        "goal_query_service": goal_query_service,
        # Module
        "module_command_service": module_command_service,
        "module_query_service": module_query_service,
        # Plan
        "plan_command_service": plan_command_service,
        "plan_query_service": plan_query_service,
        "plan_time_command_service": plan_time_command_service,
        "plan_time_query_service": plan_time_query_service,

        # Subscription
        "subscription_command_service": subscription_command_service,
        "subscription_query_service" : subscription_query_service,
        # User Goal
        "user_goal_command_service": user_goal_command_service,

        # District
        "district_command_service": district_command_service,

        # Inscription Level
        "inscription_level_command_service": inscription_level_command_service,
      "inscription_level_query_service":inscription_level_query_service,

        # Royalties
        "royalties_command_service": royalties_command_service,
        "royalties_query_service": royalties_query_service,

        # User
        "user_command_service": user_command_service,
        "user_query_service": user_query_service,
        "user_flow_service": user_flow_service,

        # --- Percent Commission ---
        "percent_commission_command_service": percent_commission_command_service,
        "percent_commission_query_service": percent_commission_query_service,

        # --- Franchise Discount ---
        "franchise_discount_command_service": franchise_discount_command_service,
        "franchise_discount_query_service": franchise_discount_query_service,

        # --- Franchise Overpriced ---
        "franchise_overpriced_command_service": franchise_overpriced_command_service,
        "franchise_overpriced_query_service": franchise_overpriced_query_service,

        # --- Franchise Config ---
        "franchise_config_command_service": franchise_config_command_service,
        "franchise_config_query_service": franchise_config_query_service,




        # Repositorios (por si los necesitas directo)
        "application_repo": application_repo,
        "card_repo": card_repo,
        "commission_repo": commission_repo,
        "goal_repo": goal_repo,
        "module_repo": module_repo,
        "plan_repo": plan_repo,
        "plan_module_repo": plan_module_repo,
        "subscription_repo": subscription_repo,
        "user_goal_repo": user_goal_repo,
        "district_repo": district_repo,
        "inscription_level_repo": inscription_level_repo,
        "royalties_repo": royalties_repo,
        "user_repo": user_repo,
        "percent_commission_repo": percent_commission_repo,
        "franchise_discount_repo": franchise_discount_repo,
        "franchise_overpriced_repo": franchise_overpriced_repo,
        "franchise_config_repo": franchise_config_repo,
    }
