"""Tests for getting data."""
import pytest
from mars_mcd_helper.get_mars_data import fetch_data, generate_fn, FetchingError


def test_generate_fn():
    """Test generating filename."""
    assert generate_fn(var1="this", var2="that", num=7) == "marsdata_var1_this-var2_that-num_7.txt"


def test_fetch_data(tmp_path):
    """Smoke Test fetching data from the server.

    Args:
        tmp_path: a pytest tmp_path fixture.
    """
    fn = fetch_data(outdir=tmp_path, ls=87.3).dataf
    assert fn.exists()


def test_fetching_error(tmp_path, mocker):
    mocked_get = mocker.patch("requests.get")
    mocked_get.return_value.text = "<html><body>Ooops! mocked error</body></html>"
    with pytest.raises(FetchingError, match="<html><body>Ooops! mocked error</body></html>"):
        fetch_data(outdir=tmp_path)
