"""
Convenience functions to call everything.

Anything implemented here should be caching.
"""
from pathlib import Path
from typing import Optional, Tuple

from .get_mars_data import fetch_data, generate_fn
from .read_mars_data import read_ascii_data


def get_parse_data(**kwargs) -> Tuple[dict, Optional[Path]]:
    """Get and parse data.

    This is a convenience function.  It first checks for
    already downloaded data and uses that in preference.

    Args:
        **kwargs: to pass to fetch.  See the documentation of `fetch_data`.

    Returns:
        (dict): The data.

    """
    if "outdir" not in kwargs:
        kwargs["outdir"] = Path(".")
    elif isinstance(kwargs["outdir"], str):
        kwargs["outdir"] = Path(kwargs["outdir"])
    params = {k: v for k, v in kwargs.items() if k not in {"outdir", "get_img", "get_data"}}  # type: ignore
    dataf = kwargs["outdir"] / generate_fn(**params)
    if dataf.exists():
        kwargs["fetch_data"] = False
    imgf = dataf.with_suffix(".png")
    if "get_img" not in kwargs:
        kwargs["get_img"] = False
    get_data = not dataf.exists()
    get_img = kwargs["get_img"] and not imgf.exists()
    if any((get_data, get_img)):
        fetch_data(**kwargs)

    return read_ascii_data(dataf), imgf if kwargs["get_img"] else None
