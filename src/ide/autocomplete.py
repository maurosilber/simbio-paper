from poincare import Constant, Parameter, System, Variable, assign, initial


class Model(System):
    a: Constant = assign(default=1, constant=True)
    b: Variable = initial(default=a)
    c: Parameter = assign(default=2)
    d: Variable = initial(default=c)
    e = d.derive() << a + c * d

Model.
