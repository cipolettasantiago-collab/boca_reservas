"""Fail-closed monitor state. Never infer availability from an empty map."""
from dataclasses import dataclass
from enum import Enum

class State(str, Enum):
    AUTH_REQUIRED = "auth_required"
    MAP_ERROR = "map_error"
    NO_AVAILABILITY = "no_availability"
    POSSIBLE_AVAILABILITY = "possible_availability"
    CONFIRMED_AVAILABILITY = "confirmed_availability"

@dataclass(frozen=True)
class Observation:
    authenticated: bool
    map_loaded: bool
    sector_count: int
    eligible_sector_ids: tuple[str, ...] = ()
    seats_verified: bool = False

def classify(o: Observation) -> State:
    if not o.authenticated:
        return State.AUTH_REQUIRED
    if not o.map_loaded or o.sector_count < 1:
        return State.MAP_ERROR
    if not o.eligible_sector_ids:
        return State.NO_AVAILABILITY
    return State.CONFIRMED_AVAILABILITY if o.seats_verified else State.POSSIBLE_AVAILABILITY
