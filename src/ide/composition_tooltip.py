from poincare import System, Variable, initial  # noqa: I001

from .constant import Model







class BigModel(System):
    my_var: Variable = initial(default=1)
    subsystem = Model()
    wrong_type = Model(c=my_var)
    wrong_variable_name = Model(z=my_var)