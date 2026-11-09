import sys
from logger_setup import get_logger
from parser import parse
from geo import ip_to_country, load_countries
from stats import failed_by_country, success_by_user, failed_invalid_user
from dashboard import show_dashboard
from graph import show_graphs

log = get_logger("main")

DEFAULT_FILE = "data/auth_log.1"


def main():
    paths = sys.argv[1:] or [DEFAULT_FILE]
    log.info(f"Starting analysis of {paths}")

    events = []
    for path in paths:
        events += parse(path)

    if not events:
        print(f"No events found in {paths}. See logs/ for details.")
        log.error(f"No events to analyse for {paths}")
        return

    load_countries([e["ip"] for e in events if e["status"] == "failed"])

    by_country = failed_by_country(events, ip_to_country)
    by_user = success_by_user(events)
    invalid_users = failed_invalid_user(events)

    show_dashboard(by_country, by_user, invalid_users)
    show_graphs(by_country, by_user, invalid_users)
    log.info("Analysis finished")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log.error(f"Fatal error: {e}")
        print("Fatal error. See logs/main.log")