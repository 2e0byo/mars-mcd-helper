# mars-MCD-helper

[![ci](https://github.com/2e0byo/mars-mcd-helper/workflows/ci/badge.svg)](https://github.com/2e0byo/mars-mcd-helper/actions?query=workflow%3Aci)
[![documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat)](https://2e0byo.github.io/mars-mcd-helper/)
[![pypi version](https://img.shields.io/pypi/v/mars-mcd-helper.svg)](https://pypi.org/project/mars-mcd-helper/)
[![gitter](https://badges.gitter.im/join%20chat.svg)](https://gitter.im/mars-mcd-helper/community)

Utilities for retrieving and processing data from the Mars Climate Database.

Currently nothing more than an interface to
[www-mars.lmd.jussie.fr](http://www-mars.lmd.jussieu.fr/mcd_python).  Note that
this tool is not in any way affiliated with that excellent project.  It is
simply a requests-based scraper.  Overuse or repetitive fetching could result in
ratelimiting or banning from `jussieu.fr`.



## Usage

```python
from mars_mcd_helper import fetch_data, read_ascii_data
outf, imgf = fetch_data(outdir=".", get_img=True, ls=87.4)
sections = read_ascii_data(outf)
print("Image to compare at", imgf)
```

## Requirements

mars-MCD-helper requires Python 3.7 or above.

<details>
<summary>To install Python 3.7, I recommend using <a href="https://github.com/pyenv/pyenv"><code>pyenv</code></a>.</summary>

```bash
# install pyenv
git clone https://github.com/pyenv/pyenv ~/.pyenv

# setup pyenv (you should also put these three lines in .bashrc or similar)
export PATH="${HOME}/.pyenv/bin:${PATH}"
export PYENV_ROOT="${HOME}/.pyenv"
eval "$(pyenv init -)"

# install Python 3.7
pyenv install 3.7.12

# make it available globally
pyenv global system 3.7.12
```
</details>

## Installation

With `pip`:
```bash
python -m pip install mars-mcd-helper # or
python3.7 -m pip install mars-mcd-helper
```

With [`pipx`](https://github.com/pipxproject/pipx):
```bash
python3.7 -m pip install --user pipx

pipx install --python python3.7 mars-mcd-helper
```

