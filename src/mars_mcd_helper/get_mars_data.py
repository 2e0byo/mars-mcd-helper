"""
This module handles getting data from the MCD by scraping the cgi interface.

We simply pass parameters up in the url, like the web version interface does.
Then we scrape the resulting web page for the link to the data and (optionally)
the image[s].


Note that this is a simple scraper and is not in any sense affiliated with the
MCD project.  Please do not run it against the server too often or
unreasonably.  Where possible use the saved output (this is why we provide a
saved output).
"""
from collections import namedtuple
from logging import getLogger
from pathlib import Path
from typing import Union

import requests
from bs4 import BeautifulSoup

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
"""Parameters which can be passed to the server.  Defaults set here are
extracted from the web interface.  Any parameter set to `None` will not be
passed.  To pass `"none"` use a string.  Do not override this dict directly;
rather pass the parameter and value as keyword arguments to `fetch_data()`."""


urlbase = "http://www-mars.lmd.jussieu.fr/mcd_python/"
url = urlbase + "cgi-bin/mcdcgi.py"
_FetchedFiles = namedtuple("_FetchedFiles", ["dataf", "imgf"])


def generate_fn(**params) -> str:
    """
    Generate a unique filename from given params.

    This function is used
    internally with the parameters used by `fetch_data()`.  It is provided here
    in case you need to generate the filename from a given set of params.

    Args:
        **params: params to consider.

    Returns:
        (str): Fn from params.
    """
    fn = "-".join(f"{k}_{x}" for k, x in params.items() if x is not None)
    return f"marsdata_{fn}.txt"


class FetchingError(Exception):
    """
    Error fetching resource.

    The server returns `200` with an html error
    message, so we raise an exception and pass the error message up.
    """


def fetch_data(outdir: Union[Path, str] = ".", get_data: bool = True, get_img: bool = False, **params):
    """
    Fetch data from the MCD and save in outdir.

    Keyword arguments (other
    than `outdir`) will override the defaults in `base_params`.

    Args:
        outdir (Union[Path, str]): dir to save in (Default value = ".")
        get_data (bool): get data or not (Default value = True)
        get_img (bool): get img or not (Default value = False)
        **params: Parameters to override.

    Raises:
        FetchingError: Failed to fetch requested data.

    Returns:
        (Path): output file.

    Call this function to retrieve data from the server and save it in a file.
    Keyword arguments passed here will override the defaults in `base_params`,
    e.g.:

    ```python
    >> fetch_data(ls=0.5, localtime=1).dataf
    Path("marsdata_ls_0.5-localtime_1.txt")
    ```
    For more information on any particular parameter see the web interface.
    """
    p = base_params.copy()
    p.update(params)
    logger.info("Fetching page")
    r = requests.get(url, params=p)
    if "Ooops!" in r.text:
        raise FetchingError(f"Failed to download, server said {r.text}")
    print(r, r.text)
    soup = BeautifulSoup(r.text, features="html.parser")
    if isinstance(outdir, str):
        outdir = Path(outdir).expanduser().resolve()

    dataf, imgf = None, None

    if get_data:
        data_url = urlbase + soup.body.a["href"].replace("../", "")
        logger.info(f"Fetching ascii data from {data_url}")
        r = requests.get(data_url)
        dataf = outdir / generate_fn(**params)
        with dataf.open("w") as f:
            f.write(r.text)

    if get_img:
        img_url = urlbase + soup.body.img["src"].replace("../", "")
        logger.info(f"Fetching img from {img_url}")
        r = requests.get(img_url)
        imgf = (outdir / generate_fn(**params)).with_suffix(".png")
        with imgf.open("wb") as im:
            im.write(r.content)

    return _FetchedFiles(dataf, imgf)
