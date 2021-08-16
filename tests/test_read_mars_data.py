import pytest
import numpy as np

from mars_mcd_helper.read_mars_data import parse_header, parse_body, parse_number, read_ascii_data
from datetime import datetime
from pathlib import Path

cases = [["12", 12], ["12.0008", 12.0008], ["----", None], ["1e78", 1e78]]


@pytest.mark.parametrize("x,y", cases)
def test_parse_number(x, y):
    assert parse_number(x) == y


def test_parse_body():
    body = """---- ||   -9.00000e+01   -8.61702e+01   -8.23404e+01   -7.85106e+01   -7.46809e+01   -7.08511e+01   -6.70213e+01   -6.31915e+01   -5.93617e+01   -5.55319e+01   -5.17021e+01   -4.78723e+01   -4.40426e+01   -4.02128e+01   -3.63830e+01   -3.25532e+01   -2.87234e+01   -2.48936e+01   -2.10638e+01   -1.72340e+01   -1.34043e+01   -9.57447e+00   -5.74468e+00   -1.91489e+00    1.91489e+00    5.74468e+00    9.57447e+00    1.34043e+01    1.72340e+01    2.10638e+01    2.48936e+01    2.87234e+01    3.25532e+01    3.63830e+01    4.02128e+01    4.40426e+01    4.78723e+01    5.17021e+01    5.55319e+01    5.93617e+01    6.31915e+01    6.70213e+01    7.08511e+01    7.46809e+01    7.85106e+01    8.23404e+01    8.61702e+01    9.00000e+01
-----------------------------------
-180 ||    3.85941e-07    3.54776e-07    3.12143e-07    3.26378e-07    4.40781e-07    6.51328e-07    9.64859e-07    1.58060e-06    3.46786e-06    1.03584e-05    3.59026e-05    1.14634e-04    3.10848e-04    6.85023e-04    1.28657e-03    1.96361e-03    2.84410e-03    3.58751e-03    3.96411e-03    4.58151e-03    6.70365e-03    7.33091e-03    8.40377e-03    1.01448e-02    1.17229e-02    1.28424e-02    1.37919e-02    1.40092e-02    1.55745e-02    1.68401e-02    1.80063e-02    2.04580e-02    2.46005e-02    2.97717e-02    3.41619e-02    3.71240e-02    3.91904e-02    4.19624e-02    4.46246e-02    4.73612e-02    5.17239e-02    5.51091e-02    5.86257e-02    6.15134e-02    6.02517e-02    4.47480e-02    2.85537e-02    1.91096e-02"""
    body = body.split("\n")
    resp = parse_body(body)
    xlabels = [
        -9.00000e01,
        -8.61702e01,
        -8.23404e01,
        -7.85106e01,
        -7.46809e01,
        -7.08511e01,
        -6.70213e01,
        -6.31915e01,
        -5.93617e01,
        -5.55319e01,
        -5.17021e01,
        -4.78723e01,
        -4.40426e01,
        -4.02128e01,
        -3.63830e01,
        -3.25532e01,
        -2.87234e01,
        -2.48936e01,
        -2.10638e01,
        -1.72340e01,
        -1.34043e01,
        -9.57447e00,
        -5.74468e00,
        -1.91489e00,
        1.91489e00,
        5.74468e00,
        9.57447e00,
        1.34043e01,
        1.72340e01,
        2.10638e01,
        2.48936e01,
        2.87234e01,
        3.25532e01,
        3.63830e01,
        4.02128e01,
        4.40426e01,
        4.78723e01,
        5.17021e01,
        5.55319e01,
        5.93617e01,
        6.31915e01,
        6.70213e01,
        7.08511e01,
        7.46809e01,
        7.85106e01,
        8.23404e01,
        8.61702e01,
        9.00000e01,
    ]
    data = np.array(
        [
            [
                "3.85941e-07",
                "3.54776e-07",
                "3.12143e-07",
                "3.26378e-07",
                "4.40781e-07",
                "6.51328e-07",
                "9.64859e-07",
                "1.58060e-06",
                "3.46786e-06",
                "1.03584e-05",
                "3.59026e-05",
                "1.14634e-04",
                "3.10848e-04",
                "6.85023e-04",
                "1.28657e-03",
                "1.96361e-03",
                "2.84410e-03",
                "3.58751e-03",
                "3.96411e-03",
                "4.58151e-03",
                "6.70365e-03",
                "7.33091e-03",
                "8.40377e-03",
                "1.01448e-02",
                "1.17229e-02",
                "1.28424e-02",
                "1.37919e-02",
                "1.40092e-02",
                "1.55745e-02",
                "1.68401e-02",
                "1.80063e-02",
                "2.04580e-02",
                "2.46005e-02",
                "2.97717e-02",
                "3.41619e-02",
                "3.71240e-02",
                "3.91904e-02",
                "4.19624e-02",
                "4.46246e-02",
                "4.73612e-02",
                "5.17239e-02",
                "5.51091e-02",
                "5.86257e-02",
                "6.15134e-02",
                "6.02517e-02",
                "4.47480e-02",
                "2.85537e-02",
                "1.91096e-02",
            ]
        ],
        dtype="<U11",
    )
    assert len(resp.xlabels) == len(xlabels)
    assert resp.xlabels == pytest.approx(xlabels)
    assert resp.ylabels == [-180]
    assert (resp.data == data).all()


def test_parse_header():
    data = """##########################################################################################
### MCD_v5.3 with climatology average solar scenario.
### Ls 85.3deg. Altitude 10.0 m ALS Local time 0.0h (at longitude 0) 
### --------------------------------------------------------------------------------------
### Column 1 is East longitude (degrees)
### Columns 2+ are Water vapor column (kg/m2)
### Line 1 is North latitude (degrees)
### --------------------------------------------------------------------------------------
### Retrieved on: 2021-08-14T16:27:39.703997
### Mars Climate Database (c) LMD/OU/IAA/ESA/CNES
##########################################################################################"""
    data = data.split("\n")
    resp = parse_header(data[1:])
    assert resp["mcd_version"] == "v5.3"
    assert resp["model"] == "climatology average solar scenario"
    assert resp["ls"] == "85.3deg"
    assert resp["altitude"] == "10.0 m"
    assert resp["local_time"] == "0.0h (at longitude 0)"
    assert resp["column_1"] == "East longitude (degrees)"
    assert resp["variable"] == "Water vapor column (kg/m2)"
    assert resp["keys"] == "North latitude (degrees)"
    assert resp["retrieval_date"] == datetime(2021, 8, 14, 16, 27, 39, 703997)


def test_parse_file():
    sections = read_ascii_data(Path("tests/data.txt"))
    assert list(sections.keys()) == [
        "Water vapor column (kg/m2)",
        "Temperature (K)",
        "Pressure (Pa)",
    ]
    for k, v in sections.items():
        assert len(v["data"].data) == 64
