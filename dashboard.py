from logger_setup import get_logger

log = get_logger("dashboard")

MAX_BAR = 40


def print_section(title, counter):
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)
    try:
        if not counter:
            print("  (no data)")
            log.warning(f"Empty section: {title}")
            return
        top = counter.most_common(10)
        biggest = top[0][1]
        for name, count in top:
            bar = "#" * max(1, round(count / biggest * MAX_BAR))
            print(f"  {name:<18} {bar} {count}")
    except Exception as e:
        log.error(f"Error displaying '{title}': {e}")
        print("  (display error)")


def show_dashboard(by_country, by_user, invalid_users):
    print_section("1. Failed attempts per country (top 10)", by_country)
    print_section("2. Successful attempts per user", by_user)
    print_section("3. Failed attempts with invalid user (top 10)", invalid_users)
    print()