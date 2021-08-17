"""Utilities for retrieving and processing data from the Mars Climate Database."""

from pathlib import Path
from typing import List, Optional, Tuple

from .get_mars_data import fetch_data, generate_fn
from .read_mars_data import read_ascii_data

__all__: List[str] = []  # noqa: WPS410 (the only __variable__ we use)


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
    params = {k: v for k, v in kwargs if k not in {"outdir", "fetch_img", "fetch_data"}}  # type: ignore
    dataf = kwargs["outdir"] / generate_fn(**params)
    imgf = dataf.with_suffix("png")
    if "fetch_img" not in kwargs:
        kwargs["fetch_img"] = False
    get_data = not dataf.exists()
    get_img = kwargs["fetch_img"] and not imgf.exists()
    if any((get_data, get_img)):
        dataf, imgf = fetch_data(**kwargs)
    return read_ascii_data(dataf), imgf if kwargs["fetch_img"] else None
