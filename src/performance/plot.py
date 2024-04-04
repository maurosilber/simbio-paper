from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure
from scipy.stats import iqr


@dataclass
class Metadata:
    name: str
    color: str


def load_and_summarize(p: Path):
    def load_one_and_melt(p: Path):
        return (
            pd.read_csv(p, index_col=0)
            .drop(columns="t_end")
            .assign(cold=lambda x: x.load + x.first_run)
            .melt(["model_id"])
            .assign(method=p.parent.stem)
        )

    dfs = pd.concat(map(load_one_and_melt, p.rglob("*.csv")))
    return dfs.groupby(["variable", "method", "model_id"])["value"].agg(["median", iqr])


def plot_number_of_points(
    fig: Figure,
    df: pd.DataFrame,
    model_id: str,
    metadata: dict[str, Metadata],
):
    df_model = (
        df.reset_index()
        .set_index("model_id")
        .loc[model_id]
        .set_index("variable")
        .drop(index=["cold", "first_run", "load"])
        .reset_index()
        .astype({"variable": float})
        .sort_values("variable")
    )

    ax = fig.add_subplot()
    ax.set_xlabel("Number of evaluated time points")
    ax.set_ylabel("Run time [s]")
    ax.set_xlim(5e0, 5e3)
    ax.set_ylim(1e-4, 2e-2)
    ax.set_xscale("log")
    ax.set_yscale("log")

    for method, data in df_model.groupby("method"):
        ax.errorbar(
            x=data["variable"],
            y=data["median"],
            yerr=data["iqr"],
            fmt="--o",
            capsize=3,
            color=metadata[method].color,
            label=metadata[method].name,
        )


def plot_runtime(
    fig: Figure,
    df: pd.DataFrame,
    metadata: dict[str, Metadata],
):
    ax = fig.add_subplot()
    ax.set_ylabel("Run time [s]")
    ax.set_xlabel("Geometric mean run time [s]")

    n_points = "300"
    df = df.reset_index().set_index("variable").loc[n_points].reset_index(drop=True)
    df = df.join(
        df.groupby("model_id")["median"].agg("median").rename("x"),
        on="model_id",
    )

    ax.axline((1e-3, 1e-3), slope=1, color="black")
    for method, data in df.groupby("method"):
        ax.errorbar(
            x=data["x"],
            y=data["median"],
            yerr=data["iqr"],
            capsize=1,
            capthick=3,
            linestyle="",
            color=metadata[method].color,
        )
    ax.set(xscale="log", yscale="log")


if __name__ == "__main__":
    import sys

    import matplotlib.pyplot as plt
    import seaborn

    metadata = {
        "copasi": Metadata(name="COPASI", color="C0"),
        "roadrunner": Metadata(name="RoadRunner", color="C1"),
        "simbio-numpy-lsoda": Metadata(name="SimBio with\nNumPy", color="C2"),
        "simbio-numba-lsoda": Metadata(name="SimBio with\nNumba", color="C3"),
        "simbio-numba-numbalsoda": Metadata(name="SimBio with\nnumbalsoda", color="C4"),
    }

    path = Path(__file__).parent
    df = load_and_summarize(path / "results")

    fig = plt.figure(layout="constrained", figsize=(8, 2.5))
    figs = fig.subfigures(ncols=3, width_ratios=[1, 0.7, 1])
    plot_number_of_points(figs[0], df, "BIOMD3", metadata)
    plot_runtime(figs[2], df, metadata)
    fig.legend(loc="center", bbox_to_anchor=(0.5, 0.5), frameon=False)
    seaborn.despine(fig)

    match sys.argv[1:]:
        case ["save"]:
            for format in ["png", "pdf", "svg"]:
                fig.savefig(path / f"figures/performance.{format}")
        case _:
            plt.show()
