import requests
from bs4 import BeautifulSoup
from devtools import debug

"""
http://www-mars.lmd.jussieu.fr/mcd_python/cgi-bin/mcdcgi.py
?datekeyhtml=1
&ls=85.3
&localtime=0.
&year=2021
&month=8
&day=14
&hours=14
&minutes=26
&seconds=12
&julian=2459441.101527778
&martianyear=36
&martianmonth=3
&sol=183
&latitude=all
&longitude=all
&altitude=10.
&zkey=3
&isfixedlt=off
&dust=1
&hrkey=1
&zonmean=off
&var1=mtot
&var2=t
&var3=p
&var4=none
&dpi=80
&islog=off
&colorm=Blues
&minval=
&maxval=
&proj=cyl
&plat=
&plon=
&trans=
&iswind=off
&latpoint=
&lonpoint=
"""


base_params = {
    "datekeyhtml": 1,
    "ls": 85.3,
    "localtime": 0.0,
    "year": 2021,
    "month": 8,
    "day": 14,
    "hours": 14,
    "minutes": 26,
    "seconds": 12,
    "julian": "2459441.101527778",
    "martianyear": 36,
    "martianmonth": 3,
    "sol": 183,
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


url = "http://www-mars.lmd.jussieu.fr/mcd_python/cgi-bin/mcdcgi.py"


def fetch_data(**params):
    p = base_params.copy()
    p.update(params)
    debug(p)
    r = requests.get(url, params=p)
    if "Ooops!" in r.text:
        debug(r.url)
        raise Exception(f"Failed to download, server said {r.text}")

    debug(r.text)


if __name__ == "__main__":
    fetch_data()
