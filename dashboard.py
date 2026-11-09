from logger_setup import get_logger

log = get_logger("dashboard")


def print_section(title, counter):
    print()
    print("=" * 40)
    print(title)
    print("=" * 40)
    try:
        if not counter:
            print("  (no data)")
            log.warning(f"Empty section: {title}")
            return
        for name, count in counter.most_common():
            print(f"  {name:<20} {'#' * count} {count}")
    except Exception as e:
        log.error(f"Error displaying '{title}': {e}")
        print("  (display error)")


def show_dashboard(by_country, by_user, invalid_users):
    print_section("1. Failed attempts by country", by_country)
    print_section("2. Successful attempts by user", by_user)
    print_section("3. Failed attempts with invalid user", invalid_users)
    print()