from collections import Counter
from logger_setup import get_logger

log = get_logger("stats")


def failed_by_country(events, ip_to_country):
    try:
        if not events:
            log.warning("failed_by_country: no events received")
            return Counter()
        return Counter(
            ip_to_country(e["ip"]) for e in events if e["status"] == "failed"
        )
    except KeyError as e:
        log.error(f"failed_by_country: missing key {e}")
    except Exception as e:
        log.error(f"failed_by_country: unexpected error {e}")
    return Counter()


def success_by_user(events):
    try:
        if not events:
            log.warning("success_by_user: no events received")
            return Counter()
        return Counter(e["user"] for e in events if e["status"] == "success")
    except KeyError as e:
        log.error(f"success_by_user: missing key {e}")
    except Exception as e:
        log.error(f"success_by_user: unexpected error {e}")
    return Counter()


def failed_invalid_user(events):
    try:
        if not events:
            log.warning("failed_invalid_user: no events received")
            return Counter()
        return Counter(
            e["user"] for e in events if e["status"] == "failed" and e["invalid"]
        )
    except KeyError as e:
        log.error(f"failed_invalid_user: missing key {e}")
    except Exception as e:
        log.error(f"failed_invalid_user: unexpected error {e}")
    return Counter()