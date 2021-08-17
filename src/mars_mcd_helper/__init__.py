"""
mars-MCD-helper package.

Utilities for retrieving and processing data from the Mars Climate Database
"""

from typing import List

from .get_mars_data import fetch_data, generate_fn
from .read_mars_data import read_ascii_data

__all__: List[str] = []  # noqa: WPS410 (the only __variable__ we use)


def get_parse_data(**kwargs) -> dict:
    """
    Get and parse data.  This is a convenience function.  It first checks for
    already downloaded data and uses that in preference.

    Args:
        **kwargs: to pass to fetch.

    Returns:
        (dict): The data.

    """
    if "outdir" not in kwargs:
        kwargs["outdir"] = Path(".")
    elif isinstance(kwargs["outdir"], str):
        kwargs["outdir"] = Path(kwargs["outdir"])
    dataf = kwargs["outdir"] / generate_fn({k:v for k:v in params if k != "outdir"})
    if not dataf.exists():
        dataf = fetch_data(**kwargs)
    return read_ascii_data(dataf)
