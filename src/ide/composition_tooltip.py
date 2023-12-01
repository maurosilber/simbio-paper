from poincare import System, Variable, initial  # noqa: I001

from .autocomplete import Model









class BigModel(System):
    x: Variable = initial(default=1)
    wrong_name = Model(z=x)
    wrong_type = Model(a=x)