"""Tests for getting data."""
from mars_mcd_helper.get_mars_data import generate_fn, fetch_data


def test_generate_fn():
    """Test generating filename."""
    assert generate_fn(var1="this", var2="that", num=7) == "marsdata_this-that-7.txt"


def test_fetch_data(tmp_path):
    """Smoke Test fetching data from the server.

    Args:
        tmp_path: a pytest tmp_path fixture.
    """
    fn = fetch_data(outdir=tmp_path, ls=87.3)
    assert fn.exists()
