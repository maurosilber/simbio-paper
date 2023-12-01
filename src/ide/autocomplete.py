from poincare import Constant, Parameter, System, Variable, assign, initial


class Model(System):
    A: Variable = initial(default=0)
    b: Constant = assign(default=1, constant=True)
    c: Parameter = assign(default=2)


Model.
