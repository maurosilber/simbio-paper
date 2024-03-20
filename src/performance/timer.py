from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
from typing import Protocol

import pandas as pd
from biomodels import get_omex
from tqdm import tqdm

tqdm.pandas()


class Runner(Protocol):
    atol: float
    rtol: float

    def __init__(self, *, atol: float, rtol: float): ...
    def load_model(self, sbml: str): ...
    def run_model(self, *, stop: float, n_points: int): ...


@dataclass
class Model:
    sbml: str
    stop: float


def time(
    *,
    runner: Runner,
    model: Model,
    n_points: list[int],
    n_runs: int,
) -> dict[str, float]:
    time_start = perf_counter()
    runner.load_model(model.sbml)
    time_loaded = perf_counter()
    runner.run_model(stop=model.stop, n_points=n_points[0])
    time_first_run = perf_counter()

    output = {
        "load": time_loaded - time_start,
        "first_run": time_first_run - time_loaded,
    }

    for n in n_points:
        start = perf_counter()
        for _ in range(n_runs):
            runner.run_model(stop=model.stop, n_points=n)
        stop = perf_counter()
        output[str(n)] = (stop - start) / n_runs
    return output


def run_model(model_id: str, t_end: float, *, runner: type[Runner]):
    omex = get_omex(model_id)
    model = Model(
        sbml=omex.master.read_text(),
        stop=t_end,
    )
    try:
        result = time(
            runner=runner(atol=1e-9, rtol=1e-6),
            model=model,
            n_points=[10, 30, 100, 300, 1000, 3000],
            n_runs=100,
        )

    except Exception:
        raise
    else:
        return {
            "model_id": model_id,
            "t_end": t_end,
            **result,
        }


if __name__ == "__main__":
    import sys
    from functools import partial
    from pathlib import Path

    match sys.argv[1:]:
        case ["copasi"]:
            from .runners.copasi import COPASI as runner
        case ["roadrunner"]:
            from .runners.roadrunner import Tellurium as runner
        case ["simbio", "numpy", "lsoda"]:
            from .runners.simbio import LSODA, SimBio

            runner = partial(SimBio, backend="numpy", solver=LSODA)
        case ["simbio", "numpy", "cvode"]:
            from .runners.simbio import CVODE, SimBio

            runner = partial(SimBio, backend="numpy", solver=CVODE)
        case ["simbio", "numba", "lsoda"]:
            from .runners.simbio import LSODA, SimBio

            runner = partial(SimBio, backend="numba", solver=LSODA)
        case ["simbio", "numba", "numbalsoda"]:
            from .runners.simbio import LSODA, SimBio

            runner = partial(
                SimBio,
                backend="numba",
                solver=partial(LSODA, implementation="numbalsoda"),
            )
        case ["simbio", "numba", "cvode"]:
            from .runners.simbio import CVODE, SimBio

            runner = partial(SimBio, backend="numba", solver=CVODE)
        case _:
            raise ValueError(sys.argv[1:])

    output = "-".join(sys.argv[1:])

    path = Path(__file__).parent

    models = pd.read_csv(path / "models.txt")
    results: pd.DataFrame = models.progress_apply(
        lambda x: pd.Series(run_model(**x, runner=runner)),
        axis="columns",
    )
    results_dir = path / "results"
    results_dir.mkdir(exist_ok=True)
    results.to_csv(results_dir / f"{output}.csv", index=False)
