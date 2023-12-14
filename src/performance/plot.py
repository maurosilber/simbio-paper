from pathlib import Path

import pandas as pd
from matplotlib.figure import Figure


def load(file):
    return pd.read_csv(file).drop(columns="t_end").set_index("model_id")


def plot_number_of_points(fig: Figure, df: dict[str, pd.DataFrame], model_id: str):
    ax = fig.add_subplot()
    ax.set_xlabel("Number of evaluated time points")
    ax.set_ylabel("Run time [s]")
    ax.set_ylim(1e-4, 2e-2)

    times = (
        pd.DataFrame(v.loc[model_id].rename(k) for k, v in df.items())
        .drop(columns=["load", "first_run"])
        .T
    )
    times.index = times.index.astype(float)
    times.plot(ax=ax, logx=True, logy=True, marker="o", legend=False)


def plot_runtime(fig: Figure, df: dict[str, pd.DataFrame]):
    ax = fig.add_subplot()
    ax.set_ylabel("Run time [s]")
    ax.set_xlabel("Geometric mean run time [s]")

    n_points = "300"
    geom_average = 1 / sum(1 / v[n_points] for v in df.values())

    ax.axline((1e-3, 1e-3), slope=1, color="black")
    for k, v in df.items():
        ax.scatter(geom_average, v[n_points], s=5)
    ax.set(xscale="log", yscale="log")


if __name__ == "__main__":
    import sys

    import matplotlib.pyplot as plt
    import seaborn

    path = Path(__file__).parent

    files = {
        "COPASI": "copasi.csv",
        "RoadRunner": "roadrunner.csv",
        "SimBio NumPy": "simbio-numpy-lsoda.csv",
        "SimBio numba": "simbio-numba-lsoda.csv",
        "SimBio numba\nand numbalsoda": "simbio-numba-numbalsoda.csv",
    }

    df = {k: load(path / f"results/{v}") for k, v in files.items()}

    fig = plt.figure(layout="constrained", figsize=(8, 2.5))
    figs = fig.subfigures(ncols=3, width_ratios=[1, 0.7, 1])
    plot_number_of_points(figs[0], df, "BIOMD3")
    plot_runtime(figs[2], df)
    fig.legend(loc="center", bbox_to_anchor=(0.5, 0.5), frameon=False)
    seaborn.despine(fig)

    match sys.argv[1:]:
        case ["save"]:
            fig.savefig(path / "figures/performance.png")
        case _:
            plt.show()
