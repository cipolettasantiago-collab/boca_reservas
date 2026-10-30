"""Generic monitoring loop scaffold. The site adapter is intentionally not implemented.

No repeated requests are issued until a permitted authenticated adapter has been
verified against Boca Socios. Prevents falsely claiming the bot is running.
"""
import time
from monitor.state import classify, State

def monitor_once(adapter):
    observation = adapter.read_observation()
    state = classify(observation)
    if state in (State.AUTH_REQUIRED, State.MAP_ERROR):
        return {"state": state.value, "retry": False, "reason": "manual_review_required"}
    return {"state": state.value, "retry": True,
            "sectors": list(observation.eligible_sector_ids),
            "reservation_confirmed": False}

def monitor_loop(adapter, interval_seconds=60):
    if interval_seconds < 30:
        raise ValueError("No aggressive polling until site rate limits are verified")
    while True:
        event = monitor_once(adapter)
        yield event
        if not event["retry"]:
            break
        time.sleep(interval_seconds)
