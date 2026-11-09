from logger_setup import get_logger

log = get_logger("graph")

BG = "black"
BAR = "orange"
TEXT = "white"


def draw_bars(ax, counter, title, xlabel):
    ax.set_facecolor(BG)
    ax.set_title(title, color=TEXT, loc="left", fontweight="bold")
    ax.tick_params(colors=TEXT)
    for spine in ax.spines.values():
        spine.set_color(TEXT)
    if not counter:
        log.warning(f"No data for graph: {title}")
        ax.text(0.5, 0.5, "no data", ha="center", color=TEXT, transform=ax.transAxes)
        return
    top = counter.most_common(10)
    names = [n for n, _ in top]
    values = [v for _, v in top]
    bars = ax.barh(names, values, color=BAR)
    ax.invert_yaxis()
    ax.bar_label(bars, padding=3, color=TEXT)
    ax.set_xlabel(xlabel, color=TEXT)
    ax.set_xlim(0, max(values) * 1.15)


def show_graphs(by_country, by_user, invalid_users):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        log.error("matplotlib is not installed")
        print("matplotlib missing, graphs skipped.")
        return

    try:
        total_failed = sum(by_country.values())
        total_invalid = sum(invalid_users.values())
        total_success = sum(by_user.values())

        fig, axes = plt.subplots(1, 3, figsize=(16, 5.5), facecolor=BG)
        fig.suptitle("SSH AUTHENTICATION DASHBOARD", color=TEXT,
                     fontsize=16, fontweight="bold")
        fig.text(0.5, 0.90,
                 f"{total_failed} failed attempts  |  {total_invalid} with an invalid user  |  {total_success} successful",
                 color=TEXT, ha="center")

        draw_bars(axes[0], by_country, "Failed attempts per country (top 10)", "failed attempts")
        draw_bars(axes[1], by_user, "Successful attempts per user", "successful attempts")
        draw_bars(axes[2], invalid_users, "Failed attempts with invalid user", "failed attempts")

        plt.tight_layout(rect=(0, 0, 1, 0.88))
        plt.show()
    except Exception as e:
        log.error(f"Error drawing graphs: {e}")