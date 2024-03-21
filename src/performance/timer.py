from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
from typing import Protocol

from biomodels import get_omex


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
        runner.run_model(stop=model.stop, n_points=n)
        stop = perf_counter()
        output[str(n)] = stop - start
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

    import pandas as pd
    from tqdm import tqdm

    match sys.argv[1:]:
        case ["copasi"]:
            from .runners.copasi import COPASI as runner
        case ["roadrunner"]:
            from .runners.roadrunner import Tellurium as runner
        case ["simbio-numpy-lsoda"]:
            from .runners.simbio import LSODA, SimBio

            runner = partial(SimBio, backend="numpy", solver=LSODA)
        case ["simbio-numpy-cvode"]:
            from .runners.simbio import CVODE, SimBio

            runner = partial(SimBio, backend="numpy", solver=CVODE)
        case ["simbio-numba-lsoda"]:
            from .runners.simbio import LSODA, SimBio

            runner = partial(SimBio, backend="numba", solver=LSODA)
        case ["simbio-numba-numbalsoda"]:
            from .runners.simbio import LSODA, SimBio

            runner = partial(
                SimBio,
                backend="numba",
                solver=partial(LSODA, implementation="numbalsoda"),
            )
        case ["simbio-numba-cvode"]:
            from .runners.simbio import CVODE, SimBio

            runner = partial(SimBio, backend="numba", solver=CVODE)
        case _:
            raise ValueError(sys.argv[1:])

    path = Path(__file__).parent
    output_path = path / "results" / sys.argv[1]
    output_path.mkdir(exist_ok=True, parents=True)
    models = pd.read_csv(path / "times.txt")
    for _, (model_num, log_time) in tqdm(models.iterrows(), total=len(models)):
        model_id = f"BIOMD{model_num}"
        model_path = (output_path / model_id).with_suffix(".csv")
        if model_path.exists():
            continue
        result = pd.DataFrame(
            [run_model(model_id, 10.0**log_time, runner=runner) for _ in range(20)]
        )
        result.to_csv(model_path)
