"""
mars-MCD-helper package.

Utilities for retrieving and processing data from the Mars Climate Database
"""

from typing import List
from .read_mars_data import *
from .get_mars_data import *

__all__: List[str] = []  # noqa: WPS410 (the only __variable__ we use)


def get_parse_data(**kwargs):
    dataf = fetch_data(**kwargs)
    return read_ascii_data(dataf)
