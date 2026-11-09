from logger_setup import get_logger

log = get_logger("graph")


def show_graphs(by_country, by_user, invalid_users):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        log.error("matplotlib is not installed")
        print("matplotlib missing, graphs skipped.")
        return

    try:
        sections = [
            (by_country, "Failed attempts by country"),
            (by_user, "Successful attempts by user"),
            (invalid_users, "Failed attempts (invalid user)"),
        ]
        fig, axes = plt.subplots(1, 3, figsize=(15, 4))
        for ax, (counter, title) in zip(axes, sections):
            ax.set_title(title)
            if counter:
                ax.bar(list(counter.keys()), list(counter.values()))
                ax.tick_params(axis="x", rotation=45)
            else:
                log.warning(f"No data for graph: {title}")
                ax.text(0.5, 0.5, "no data", ha="center")
        plt.tight_layout()
        plt.show()
    except Exception as e:
        log.error(f"Error drawing graphs: {e}")