import gzip
import re
from logger_setup import get_logger

log = get_logger("parser")

FAILED = re.compile(r"Failed password for (invalid user )?(\S*) from (\d+\.\d+\.\d+\.\d+)")
SUCCESS = re.compile(r"Accepted \w+ for (\S+) from (\d+\.\d+\.\d+\.\d+)")


def open_log(path):
    # .gz files are read through gzip, other files as plain text
    if path.endswith(".gz"):
        return gzip.open(path, "rt", encoding="utf-8", errors="replace")
    return open(path, encoding="utf-8", errors="replace")


def parse(path):
    events = []
    ignored = 0
    try:
        with open_log(path) as f:
            for line in f:
                m = FAILED.search(line)
                if m:
                    events.append({
                        "status": "failed",
                        "invalid": m.group(1) is not None,
                        "user": m.group(2) or "(empty)",
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

                ignored += 1
    except FileNotFoundError:
        log.error(f"File not found: {path}")
    except PermissionError:
        log.error(f"Permission denied: {path}")
    except (OSError, EOFError) as e:
        log.error(f"Cannot read {path} (corrupted or not a valid file): {e}")
    except Exception as e:
        log.error(f"Unexpected parsing error: {e}")

    log.info(f"{len(events)} events parsed from {path}, {ignored} lines ignored")
    return events