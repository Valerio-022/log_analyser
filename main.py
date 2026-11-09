import sys
from logger_setup import get_logger
from parser import parse
from geo import ip_to_country
from stats import failed_by_country, success_by_user, failed_invalid_user
from dashboard import show_dashboard

log = get_logger("main")


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "data/auth.log"
    log.info(f"Starting analysis of {path}")

    events = parse(path)
    if not events:
        print(f"No events found in {path}. See logs/ for details.")
        log.error(f"No events to analyse for {path}")
        return

    by_country = failed_by_country(events, ip_to_country)
    by_user = success_by_user(events)
    invalid_users = failed_invalid_user(events)

    show_dashboard(by_country, by_user, invalid_users)
    log.info("Analysis finished")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log.error(f"Fatal error: {e}")
        print("Fatal error. See logs/main.log")