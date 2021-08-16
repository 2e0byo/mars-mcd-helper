import requests
from bs4 import BeautifulSoup
from devtools import debug
from logging import getLogger, INFO, DEBUG
from pathlib import Path

logger = getLogger(__name__)


base_params = {
    "datekeyhtml": 1,
    "ls": 85.3,
    "localtime": 0.0,
    # "year": 2021,
    # "month": 8,
    # "day": 14,
    # "hours": 14,
    # "minutes": 26,
    # "seconds": 12,
    # "julian": "2459441.101527778",
    # "martianyear": 36,
    # "martianmonth": 3,
    # "sol": 183,
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


def generate_fn(**params):
    fn = "-".join(str(x) for _, x in params.items() if x)
    return f"marsdata_{fn}.txt"


def fetch_data(outdir=".", **params):
    p = base_params.copy()
    p.update(params)
    logger.info(f"Fetching page")
    r = requests.get(url, params=p)
    if "Ooops!" in r.text:
        raise Exception(f"Failed to download, server said {r.text}")
    soup = BeautifulSoup(r.text, features="html.parser")
    data_url = urlbase + soup.body.a["href"].replace("../", "")
    logger.info(f"Fetching ascii data from {data_url}")
    r = requests.get(data_url)
    fn = Path(outdir) / generate_fn(**params)
    with fn.open("w") as f:
        f.write(r.text)
    return f
