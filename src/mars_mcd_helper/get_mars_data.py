"""Get data from the MCD by scraping the cgi interface."""
import requests
from bs4 import BeautifulSoup
from logging import getLogger
from pathlib import Path
from typing import Union

logger = getLogger(__name__)


base_params = {
    "datekeyhtml": 1,
    "ls": 85.3,
    "localtime": 0.0,  # noqa
    "year": None,
    "month": None,
    "day": None,
    "hours": None,
    "minutes": None,
    "seconds": None,
    "julian": None,
    "martianyear": None,
    "martianmonth": None,
    "sol": None,
    "latitude": "all",
    "longitude": "all",
    "altitude": 10.0,
    "zkey": 3,
    "isfixedlt": "off",
    "dust": 1,
    "hrkey": 1,
    "zonmean": "off",
    "var1": "mtot",
    "var2": "t",
    "var3": "p",
    "var4": "none",
    "dpi": 80,
    "islog": "off",
    "colorm": "Blues",
    "minval": None,
    "maxval": None,
    "proj": "cyl",
    "plat": None,
    "plon": None,
    "trans": None,
    "iswind": "off",
    "latpoint": None,
    "lonpoint": None,
}


urlbase = "http://www-mars.lmd.jussieu.fr/mcd_python/"
url = urlbase + "cgi-bin/mcdcgi.py"


def generate_fn(**params) -> str:
    """Generate a unique filename from given params.

    Args:
        **params: params to consider.

    Returns:
        (str): Fn from params.
    """
    fn = "-".join(str(x) for _, x in params.items() if x)
    return f"marsdata_{fn}.txt"


class FetchingError(Exception):
    """Error fetching resource."""


def fetch_data(outdir: Union[Path, str] = ".", **params):
    """Fetch data from the MCD and save in outdir.

    Args:
        outdir (Union[Path, str]): dir to save in (Default value = ".")
        **params: Parameters to override.

    Raises:
        FetchingError: Failed to fetch requested data.

    Returns:
        (Path): output file.
    """
    p = base_params.copy()
    p.update(params)
    logger.info("Fetching page")
    r = requests.get(url, params=p)
    if "Ooops!" in r.text:
        raise FetchingError(f"Failed to download, server said {r.text}")
    soup = BeautifulSoup(r.text, features="html.parser")
    data_url = urlbase + soup.body.a["href"].replace("../", "")
    logger.info(f"Fetching ascii data from {data_url}")
    r = requests.get(data_url)
    if isinstance(outdir, str):
        outdir = Path(outdir).expanduser().resolve()
    fn = outdir / generate_fn(**params)
    with fn.open("w") as f:
        f.write(r.text)
    return fn
