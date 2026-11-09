import re
from logger_setup import get_logger

log = get_logger("parser")

FAILED = re.compile(r"Failed password for (invalid user )?(\S+) from (\d+\.\d+\.\d+\.\d+)")
SUCCESS = re.compile(r"Accepted \w+ for (\S+) from (\d+\.\d+\.\d+\.\d+)")


def parse(path):
    events = []
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            for n, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue

                m = FAILED.search(line)
                if m:
                    events.append({
                        "status": "failed",
                        "invalid": m.group(1) is not None,
                        "user": m.group(2),
                        "ip": m.group(3),
                    })
                    continue

                m = SUCCESS.search(line)
                if m:
                    events.append({
                        "status": "success",
                        "invalid": False,
                        "user": m.group(1),
                        "ip": m.group(2),
                    })
                    continue

                log.warning(f"Line {n} not recognised: {line}")
    except FileNotFoundError:
        log.error(f"File not found: {path}")
    except PermissionError:
        log.error(f"Permission denied: {path}")
    except Exception as e:
        log.error(f"Unexpected parsing error: {e}")

    log.info(f"{len(events)} events parsed from {path}")
    return events