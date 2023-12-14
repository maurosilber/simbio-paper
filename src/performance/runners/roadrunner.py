from dataclasses import dataclass

import tellurium

from ..timer import Runner


@dataclass
class Tellurium(Runner):
    atol: float
    rtol: float

    def load_model(self, sbml: str):
        self.runner = tellurium.loadSBMLModel(sbml)
        return self

    def run_model(self, *, stop: float, n_points: int):
        self.runner.reset()
        self.runner.integrator = "cvode"
        self.runner.integrator.absolute_tolerance = self.atol
        self.runner.integrator.relative_tolerance = self.rtol
        self.runner.integrator.variable_step_size = True
        return self.runner.simulate(0, stop, n_points)
