"""
mars-MCD-helper package.

Utilities for retrieving and processing data from the Mars Climate Database
"""

from typing import List
from .read_mars_data import read_ascii_data
from .get_mars_data import fetch_data

__all__: List[str] = []  # noqa: WPS410 (the only __variable__ we use)


def get_parse_data(**kwargs) -> dict:
    """
    Get and parse data.  This is a convenience function.

    Args:
        **kwargs: to pass to fetch.

    Returns:
        (dict): The data.

    """
    dataf = fetch_data(**kwargs)
    return read_ascii_data(dataf)
