from poincare import Parameter, System, Variable, assign, initial


class BadModel(System):
    p: Parameter = assign(default=1)
    z: Variable = initial(default=p)
    eq = z.derive() << p * z

