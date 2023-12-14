from pathlib import Path

import biomodels
import pandas as pd
from pytest import mark
from sbml.pydantic import loads as sbml_loads

from .runners import copasi, simbio

path = Path(__file__).parent
t_end = pd.read_csv(path / "models.txt").set_index("model_id")["t_end"]

tol = dict(atol=1e-6, rtol=1e-6)
tol_compare = dict(atol=1e-2, rtol=1e-2)


@mark.parametrize("model_id", t_end.index)
def test_results(model_id: str):
    t = t_end[model_id]
    zipfile = biomodels.get_omex(model_id).master
    sbml = zipfile.read_text()

    runners = [
        copasi.COPASI(**tol),
        simbio.SimBio(**tol, solver=simbio.LSODA, backend="numpy"),
    ]

    result_copasi, result_simbio = (
        r.load_model(sbml).run_model(stop=t, n_points=1000) for r in runners
    )

    result_copasi.index = result_copasi.index.rename("time").round(3)
    result_simbio.index = result_simbio.index.rename("time").round(3)

    sbml = sbml_loads(zipfile.read_bytes())
    name_mapping = {s.id: s.name for s in sbml.model.species if s.name is not None}

    def renamer_copasi(x: str):
        if x.startswith("Values["):
            return x.removeprefix("Values[").removesuffix("]")
        return x

    result_copasi = result_copasi.rename(columns=renamer_copasi)
    result_simbio = result_simbio.rename(columns=name_mapping)

    common_columns = result_simbio.columns.intersection(result_copasi.columns)

    pd.testing.assert_frame_equal(
        result_copasi[common_columns],
        result_simbio[common_columns],
        **tol_compare,
    )
