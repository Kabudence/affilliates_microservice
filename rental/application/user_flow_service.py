from datetime import datetime, timedelta, timezone
from typing import Optional
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from flask import current_app

from rental.domain.entities.commissions import CommissionsTypes
from rental.domain.entities.subscription import SubscriptionStatus
from users.domain.model.entities.user import User, UserType


class UserFlowService:
    def __init__(
        self,
        user_goal_command_service,
        user_command_service,
        user_query_service,
        subscription_command_service,
        commission_command_service,
        plan_query_service,
        goal_query_service
    ):
        self.user_goal_command_service = user_goal_command_service
        self.subscription_command_service = subscription_command_service
        self.commission_command_service = commission_command_service
        self.plan_query_service = plan_query_service
        self.user_command_service= user_command_service
        self.user_query_service = user_query_service
        self.goal_query_service = goal_query_service

    @staticmethod
    def _safe_zoneinfo(key: str):
        try:
            return ZoneInfo(key)
        except ZoneInfoNotFoundError:
            return timezone(timedelta(hours=-5))  # UTC-5 Lima

    def user_flow(self, user_id: int, plan_id: Optional[int] = None,plan_time_id: Optional[int] = None):
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
        goals = self.goal_query_service.list_all()
        if not goals:
            raise ValueError("No hay goals cargados en la BD")
        print("Goals cargados en la BD")
        for goal in goals:
            print(f"Goal ID: {goal.id}, Number of Clients: {goal.number_of_clients}")

        goal = min(goals, key=lambda g: g.number_of_clients)

        return self.user_goal_command_service.create(user_id=user_id, goal_id=goal.id)


    def buyer_user_flow(self, user_id: int, plan_id: int,plan_time_id:int):
        user = self.user_query_service.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        # Calcular fechas en hora Lima
        tz_lima = self._safe_zoneinfo("America/Lima")
        now = datetime.now(tz_lima)
        initial_date = now.isoformat()
        final_date = (now + timedelta(days=30)).isoformat()

        # Crear suscripción
        subscription = self.subscription_command_service.create(
            plan_id=plan_id,
            user_id=user_id,
            initial_date=initial_date,  # <-- aquí
            final_date=final_date,  # <-- aquí
            status=SubscriptionStatus.ACTIVE
        )

        if not user.user_owner_id:
            # Si no hay owner_id, está permitido, no hacer más validación
            return True

        owner_exists = self.user_query_service.get_by_id(user.user_owner_id)
        if not owner_exists:
            return True

        # Obtener información del plan para el cálculo de comisión
        plan = self.plan_query_service.get_by_id(plan_id)
        if not plan:
            raise ValueError("Plan not found")

        plan_time_query_service = current_app.config["plan_time_query_service"]
        plan_time = plan_time_query_service.get_by_id(int(plan_time_id)) if plan_time_id else None

        # Crear comisión para el usuario (tipo DIRECT, monto = 20% del precio del plan)
        commission = self.commission_command_service.create(
            user_id=user.user_owner_id,
            amount=plan_time.price * 0.2,
            type=CommissionsTypes.DIRECT,
            subscription_id=subscription.id
        )
        self.validate_state_user_goal(user.user_owner_id)
        return {
            "subscription": subscription,
            "commission": commission
        }


    def validate_state_user_goal(self, user_id: int):
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


