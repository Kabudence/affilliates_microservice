# commissions/application/_percent_commission_utils.py
from rental.domain.entities.percent_comissions import CommissionType

def coerce_commission_type(value) -> CommissionType:
    if isinstance(value, CommissionType):
        return value
    try:
        return CommissionType(value)
    except Exception:
        raise ValueError("commission_type must be 'application' or 'franchise'")

def validate_owner_and_percent(owner_id: int, percent: float) -> None:
    if owner_id is None or percent is None:
        raise ValueError("owner_id and percent are required")
    if percent < 0:
        raise ValueError("percent must be >= 0")
