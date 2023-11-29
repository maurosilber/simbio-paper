from poincare import Constant, System, Variable, assign, initial


class Model(System):
    c: Constant = assign(default=1, constant=True)
    x: Variable = initial(default=c)
    y: Variable = initial(default=c)