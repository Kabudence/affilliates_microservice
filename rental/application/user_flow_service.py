from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple, List
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from flask import current_app

from rental.domain.entities.commissions import CommissionsTypes
from rental.domain.entities.goal import GoalType
from rental.domain.entities.percent_comissions import CommissionType
from rental.domain.entities.plan import PlanType, _to_plan_type, Plan
from rental.domain.entities.subscription import SubscriptionStatus
from users.domain.model.entities.user import User, UserType


class UserFlowService:
    def __init__(
        self,
        user_goal_command_service,
        user_command_service,
        user_query_service,
        subscription_command_service,
        subscription_query_service,
        commission_command_service,
        plan_query_service,
        goal_query_service,
        plan_time_query_service,
        franchise_overpriced_query_service,
        percent_commissions_query_service

    ):
        self.user_goal_command_service = user_goal_command_service
        self.subscription_command_service = subscription_command_service
        self.subscription_query_service = subscription_query_service
        self.commission_command_service = commission_command_service
        self.plan_query_service = plan_query_service
        self.user_command_service= user_command_service
        self.user_query_service = user_query_service
        self.goal_query_service = goal_query_service
        self.plan_time_query_service = plan_time_query_service
        self.franchise_overpriced_query_service = franchise_overpriced_query_service
        self.percent_commissions_query_service = percent_commissions_query_service

    @staticmethod
    def _safe_zoneinfo(key: str):
        try:
            return ZoneInfo(key)
        except ZoneInfoNotFoundError:
            return timezone(timedelta(hours=-5))

    @staticmethod
    def _norm_pct(p: float) -> float:
        """
        Normaliza porcentaje: acepta 0–1 ó 0–100.
        Ej: 0.2 -> 0.2, 20 -> 0.2
        """
        if p is None:
            return 0.0
        return p / 100.0 if p > 1 else p

    def user_register_flow(self, user_id: int, plan_id: Optional[int] = None,plan_time_id: Optional[int] = None):
        user = self.user_query_service.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        if user.user_type == UserType.AFILIATE:
            self.seller_user_flow(user_id)
        else:
            plan = plan_id
            if plan is None:
                raise ValueError("plan_id must be provided for BUYER users.")
            self.buyer_user_flow(user_id, plan,plan_time_id)

    def seller_user_flow(self, user_id: int):
        user = self.user_query_service.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        plan = self.get_plan(user_id)
        if not plan:
            return None

        plan_type = _to_plan_type(plan.plan_type)

        # ⬇️ usa FRANCHISE para franquicia exclusiva, APPLICATION para el resto
        if plan_type == PlanType.FRANQUICIA_EXCLUSIVA:
            goals = self.goal_query_service.list_by_owner_id_and_goal_type(
                user.user_owner_id, GoalType.FRANCHISE
            )
        else:
            goals = self.goal_query_service.list_by_owner_id_and_goal_type(
                plan.app_id, GoalType.APPLICATION
            )

        if not goals:
            raise ValueError("No hay goals cargados en la BD")

        goal = min(goals, key=lambda g: g.number_of_clients)

        return self.user_goal_command_service.create(user_id=user_id, goal_id=goal.id)

    def buyer_user_flow(self, user_id: int, plan_id: int, plan_time_id: int):
        # 1) Usuario y fechas
        user = self.user_query_service.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        tz = self._safe_zoneinfo("America/Lima")
        now = datetime.now(tz)
        initial_date = now.isoformat()

        plan_time = self.plan_time_query_service.get_by_id(int(plan_time_id)) if plan_time_id else None
        if not plan_time:
            raise ValueError("plan_time not found")
        final_date = (now + timedelta(days=30 * plan_time.duration)).isoformat()

        # 2) Crear suscripción del HIJO (quien compra)
        subscription = self.subscription_command_service.create(
            plan_id=plan_id,  # ✅ ojo aquí
            user_id=user_id,
            initial_date=initial_date,
            final_date=final_date,
            status=SubscriptionStatus.ACTIVE
        )

        # 3) Si no tiene padre → fin
        parent = self.user_query_service.get_by_id(user.user_owner_id) if user.user_owner_id else None
        if not parent:
            return True

        # 4) Abuelo (si existe)
        grandparent = self.user_query_service.get_by_id(parent.user_owner_id) if getattr(parent, "user_owner_id",
                                                                                         None) else None

        # 5) Determinar si padre/abuelo son franquicia
        parent_is_franchise, parent_plan = self._is_franchise_user(parent.id)
        grand_is_franchise, grand_plan = (False, None)
        if grandparent:
            grand_is_franchise, grand_plan = self._is_franchise_user(grandparent.id)


        # 7) Flow de comisiones según árbol
        commissions_to_create: List[Tuple[int, float, str]] = []  # (user_id, amount, type)

        if parent_is_franchise:
            # Caso A: El PADRE es franquiciado → comisión solo al padre (según tu regla)
            overprice = self._get_overprice(parent.id, plan_id)
            over_amount = (overprice.extra_price * plan_time.duration) if overprice else 0.0

            amount_parent = over_amount
            commissions_to_create.append((parent.id, amount_parent, "direct"))

        elif (not parent_is_franchise) and grand_is_franchise:
            # Caso B: El ABUELO es franquiciado → comisión al padre y al abuelo

            overprice = self._get_overprice(grandparent.id, plan_id)
            over_amount = (overprice.extra_price * plan_time.duration) if overprice else 0.0
            commission_percent = self.percent_commissions_query_service.get_by_owner_and_type(grandparent.id,CommissionType.FRANCHISE)
            pct = commission_percent.percent if commission_percent else 0.0

            amount_parent = over_amount * pct
            amount_grandpa = over_amount * (1 - pct)

            commissions_to_create.append((parent.id, amount_parent,CommissionsTypes.DIRECT))
            commissions_to_create.append((grandparent.id, amount_grandpa, CommissionsTypes.REFERRED))
        else:
            # Caso C: Nadie en la línea es franquiciado → comisión normal al padre
            app_id = self.plan_query_service.get_by_id(plan_id).app_id
            commission_percent = self.percent_commissions_query_service.get_by_owner_and_type(app_id, CommissionType.APPLICATION)
            pct = commission_percent.percent if commission_percent else 0.0

            amount_parent = plan_time.price * pct
            commissions_to_create.append((parent.id, amount_parent, CommissionsTypes.DIRECT))

        # 8) Persistir comisiones
        for uid, amount, typ in commissions_to_create:
            self.commission_command_service.create(
                user_id=uid,
                amount=amount,
                type=typ,  # CommissionsTypes.DIRECT
                subscription_id=subscription.id
            )

        # 9) Validar metas (padre)
        self._validate_state_user_goal(parent.id)
        return True


    def _validate_state_user_goal(self, user_id: int):
        # Buscar los goals del usuario
        user_goals = self.user_goal_command_service.list_by_user(user_id)
        if not user_goals:
            return None

        user_goal = user_goals[0]

        # --- USO DE LA FECHA ACTUAL CON ZONA HORARIA LIMA ---
        tz_lima = self._safe_zoneinfo("America/Lima")
        initial_date = (
            datetime.fromisoformat(user_goal.initial_date)
            if isinstance(user_goal.initial_date, str)
            else user_goal.initial_date
        )
        now = datetime.now(tz_lima)
        if initial_date.tzinfo is None:
            initial_date = initial_date.replace(tzinfo=tz_lima)

        if (now - initial_date).days >= 30:
            first_day = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            user_goal.initial_date = first_day.isoformat()
            user_goal.goal_attained = False
            self.user_goal_command_service.user_goal_repo.update(user_goal)
            return

        # Si la meta está cumplida (goal_attained == True), salir
        if user_goal.goal_attained:
            return

        # Si la meta no está cumplida, obtener comisiones del usuario
        commissions = self.commission_command_service.commission_repo.get_all_by_user_id(user_id)
        num_commissions = len(commissions)


        goal = self.goal_query_service.get_by_id(user_goal.goal_id)
        if not goal:
            raise ValueError("Goal not found")

        # Si tiene suficientes comisiones, cumplir la meta y otorgar bonificación
        if num_commissions >= goal.number_of_clients:
            user_goal.goal_attained = True
            self.user_goal_command_service.user_goal_repo.update(user_goal)

            # Calcular el monto total de comisiones
            total_amount = sum(c.amount for c in commissions if hasattr(c, 'amount'))

            # total_amount  * percentage_to_bonus
            if goal.percentage_to_bonus is not None:
                reward = total_amount * goal.percentage_to_bonus
                # Guardar la comisión como REFERRED
                self.commission_command_service.create(
                    user_id=user_id,
                    amount=reward,
                    type=CommissionsTypes.DIRECT,
                    subscription_id=None
                )
                owner = self.user_query_service.get_by_id(user_id)
                super_aff_id = getattr(owner, "user_owner_id", None)

                if super_aff_id:  # ⬅️ evita user_id=None
                    self.commission_command_service.create(
                        user_id=super_aff_id,
                        amount=reward,
                        type=CommissionsTypes.REFERRED,
                        subscription_id=None,
                    )

    def get_plan(self, user_id)->Optional[Plan]:
        user = self.user_query_service.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        owner_user = self.user_query_service.get_by_id(user.user_owner_id) if user.user_owner_id else None
        if not owner_user:
            return None

        subscription = self.subscription_query_service.get_subscription_by_user_id(owner_user.id)
        if not subscription:
            return None

        plan = self.plan_query_service.get_by_id(subscription.plan_id)

        return plan

    def _is_franchise_user(self, user_id: int) -> Tuple[bool, Optional["Plan"]]:
        """Retorna (es_franquicia, plan_activo_del_usuario)."""
        subscription = self.subscription_query_service.get_subscription_by_user_id(user_id)
        if not subscription:
            return False, None
        plan = self.plan_query_service.get_by_id(subscription.plan_id)
        if not plan:
            return False, None
        plan_type = _to_plan_type(plan.plan_type)
        return (plan_type == PlanType.FRANQUICIA_EXCLUSIVA), plan

    def _get_franchise_percent(self, owner_id: int) -> float:
        """Lee PercentCommissions del franquiciado; si no hay, usa default."""
        pc = self.percent_commissions_query_service.get_by_owner_and_type(owner_id, CommissionType.FRANCHISE)
        return (pc.percent if pc else 0.20)  # TODO: tu default

    def _get_overprice(self, franchise_owner_id: int, plan_id: int):
        """Obtiene el sobreprecio configurado por el franquiciado para ese plan."""
        return self.franchise_overpriced_query_service.get_by_franchise_and_plan(franchise_owner_id, plan_id)
