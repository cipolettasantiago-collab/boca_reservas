"""Estados seguros de una solicitud. Este módulo NO reserva entradas."""
from enum import Enum
from dataclasses import dataclass
from typing import Optional

class Status(str, Enum):
    NO_SESSION = "no_session"
    WAITING = "waiting"
    AVAILABLE = "available"
    SEAT_SELECTED = "seat_selected"
    CONFIRMED = "confirmed"
    PAYMENT_PENDING = "payment_pending"
    ERROR = "error"

@dataclass(frozen=True)
class ReservationEvidence:
    match_id: str
    reservation_id: Optional[str] = None
    confirmed_by_provider: bool = False
    sector: Optional[str] = None
    seat: Optional[str] = None
    payment_url: Optional[str] = None

def reservation_confirmed(e: ReservationEvidence) -> bool:
    """No false positives from merely seeing a green sector or a cart item."""
    return bool(e.confirmed_by_provider and e.reservation_id and e.match_id and e.sector and e.seat)

def can_send_success(e: ReservationEvidence) -> bool:
    return reservation_confirmed(e)
