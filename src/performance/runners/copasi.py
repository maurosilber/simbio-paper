from dataclasses import dataclass

import basico

from ..timer import Runner


@dataclass
class COPASI(Runner):
    atol: float
    rtol: float

    def load_model(self, sbml: str):
        self.runner = basico.load_model_from_string(sbml)
        return self

    def run_model(self, *, stop: float, n_points: int):
        return basico.run_time_course(
            0,
            stop,
            n_points - 1,
            a_tol=self.atol,
            r_tol=self.rtol,
            method="lsoda",
        )
