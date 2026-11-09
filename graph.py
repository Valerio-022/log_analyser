from matplotlib.ticker import MaxNLocator   # NEW (import at the top)
from logger_setup import get_logger

log = get_logger("graph")

BG = "#0f172a"        # dark navy background
PANEL = "#1e293b"     # slightly lighter panels
TEXT = "#e2e8f0"
MUTED = "#94a3b8"
C_COUNTRY = "#22d3ee"  # cyan
C_INVALID = "#a78bfa"  # violet
C_SUCCESS = "#f472b6"  # pink


def style_axes(ax, title, color):
    ax.set_facecolor(PANEL)
    ax.set_title(title, color=color, loc="left", fontsize=12, fontweight="bold", pad=10)
    ax.tick_params(colors=TEXT, labelsize=9)
    ax.xaxis.grid(True, color=BG, linewidth=1)
    ax.set_axisbelow(True)
    for side in ("top", "right", "left", "bottom"):
        ax.spines[side].set_visible(False)


def empty(ax, title, color):
    style_axes(ax, title, color)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.text(0.5, 0.5, "no data", ha="center", va="center", color=MUTED,
            transform=ax.transAxes)


def draw_hbars(ax, counter, title, color):
    if not counter:
        log.warning(f"No data for graph: {title}")
        empty(ax, title, color)
        return
    style_axes(ax, title, color)
    top = counter.most_common(10)
    names = [n for n, _ in top]
    values = [v for _, v in top]
    bars = ax.barh(names, values, color=color, height=0.65)
    ax.set_ylim(max(len(names), 4) - 0.5, -0.5)   # keeps bars thin when there are few
    ax.bar_label(bars, padding=4, color=TEXT, fontsize=9)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))   # NEW: whole numbers only
    ax.set_xlim(0, max(values) * 1.15)


def draw_lollipop(ax, counter, title, color):
    if not counter:
        log.warning(f"No data for graph: {title}")
        empty(ax, title, color)
        return
    style_axes(ax, title, color)
    top = counter.most_common(10)
    names = [n for n, _ in top]
    values = [v for _, v in top]
    ypos = range(len(names))
    ax.hlines(ypos, 0, values, color=color, linewidth=2, alpha=0.8)
    ax.scatter(values, ypos, color=color, s=70, zorder=3)
    ax.set_yticks(list(ypos))
    ax.set_yticklabels(names)
    ax.invert_yaxis()
    for y, v in zip(ypos, values):
        ax.text(v + max(values) * 0.03, y, str(v), va="center", color=TEXT, fontsize=9)
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

        fig = plt.figure(figsize=(14, 8), facecolor=BG)
        grid = fig.add_gridspec(3, 2, height_ratios=[0.35, 1.4, 1],
                                width_ratios=[1.1, 1], hspace=0.55, wspace=0.3)

        # header with the 3 totals
        head = fig.add_subplot(grid[0, :])
        head.axis("off")
        head.text(0, 0.8, "SSH LOG ANALYSER", color=TEXT, fontsize=20,
                  fontweight="bold", transform=head.transAxes)
        kpis = [(f"{total_failed}", "failed attempts", C_COUNTRY),
                (f"{total_invalid}", "invalid user", C_INVALID),
                (f"{total_success}", "successful logins", C_SUCCESS)]
        for i, (value, label, color) in enumerate(kpis):
            x = 0.55 + i * 0.15
            head.text(x, 0.65, value, color=color, fontsize=20,
                      fontweight="bold", transform=head.transAxes)
            head.text(x, 0.2, label, color=MUTED, fontsize=9,
                      transform=head.transAxes)

        # countries: tall panel on the left
        draw_hbars(fig.add_subplot(grid[1:, 0]), by_country,
                   "Failed attempts by country (top 10)", C_COUNTRY)
        # invalid users: top right
        draw_lollipop(fig.add_subplot(grid[1, 1]), invalid_users,
                      "Failed attempts with invalid user", C_INVALID)
        # successful logins: bottom right
        draw_hbars(fig.add_subplot(grid[2, 1]), by_user,
                   "Successful attempts by user", C_SUCCESS)

        plt.show()
    except Exception as e:
        log.error(f"Error drawing graphs: {e}")