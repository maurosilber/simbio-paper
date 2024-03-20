from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Sequence

import numpy as np
import scipy.integrate
from poincare.simulator import Problem
from poincare.solvers import LSODA, Solution
from simbio import Simulator
from simbio.io.sbml import loads

from ..timer import Runner


@dataclass
class SimBio(Runner):
    atol: float
    rtol: float
    solver: type[LSODA] | type[CVODE]
    backend: Literal["numpy", "numba"]
    ignore_namespaces: Sequence[str] = (
        "jd",
        "jd2",
        "celldesigner",
        "html",
        "math",
        "sbml",
        "rdf",
        "jigcell",
    )

    def load_model(self, sbml: str):
        self.runner = Simulator(
            loads(sbml, ignore_namespaces=self.ignore_namespaces),
            backend=self.backend,
        )
        return self

    def run_model(self, *, stop: float, n_points: int):
        return self.runner.solve(
            save_at=np.linspace(0, stop, n_points),
            solver=self.solver(atol=self.atol, rtol=self.rtol),
        )


@dataclass(frozen=True, kw_only=True)
class CVODE:
    atol: float
    rtol: float

    def __call__(self, problem: Problem, *, save_at: np.ndarray):
        def func(t, y, p):
            dy = np.empty_like(y)
            return problem.rhs(t, y, p, dy)

        solver = scipy.integrate.ode(func)
        solver.set_initial_value(problem.y, float(problem.t[0]))
        solver.set_f_params(problem.p)
        solver.set_integrator("vode", atol=self.atol, rtol=self.rtol)
        out = np.empty((save_at.size, len(problem.y)))
        if save_at[0] == 0:
            out[0] = problem.y
        else:
            out[0] = solver.integrate(save_at[0], relax=True)
        for i, t in enumerate(save_at[1:-1], start=1):
            out[i] = solver.integrate(t, relax=True)
        out[-1] = solver.integrate(save_at[-1], relax=False)
        return Solution(save_at, out)
