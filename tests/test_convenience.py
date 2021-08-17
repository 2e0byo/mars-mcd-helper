import os

import pytest

from mars_mcd_helper.convenience import generate_fn, get_parse_data


def test_get_parse_both_cache(tmp_path, mocker):
    mocked_get = mocker.patch("requests.get")
    with (tmp_path / generate_fn()).open("w") as f:
        f.write("")
    with (tmp_path / generate_fn()).with_suffix(".png").open("w") as f:
        f.write("")
    data, imgf = get_parse_data(outdir=tmp_path, get_img=True)
    assert imgf.exists()
    assert not data
    mocked_get.assert_not_called()


def test_get_parse_cache_str(tmp_path, mocker):
    mocked_get = mocker.patch("requests.get")
    with (tmp_path / generate_fn()).open("w") as f:
        f.write("")
    data, imgf = get_parse_data(outdir=str(tmp_path))
    assert not imgf
    assert not data
    mocked_get.assert_not_called()


def test_get_parse_cache_none(tmp_path, mocker):
    mocked_get = mocker.patch("requests.get")
    mocked_get.return_value.text = f"<html><body><a href='here'>link</a><img src='there'/></body></html>"
    with (tmp_path / generate_fn()).open("w") as f:
        f.write("")
    os.chdir(tmp_path)
    data, imgf = get_parse_data()
    assert not imgf
    assert not data
    mocked_get.assert_not_called()


def test_get_parse_both_nocached(tmp_path, mocker):
    mocked_get = mocker.patch("requests.get")
    mocked_get.return_value.text = f"<html><body><a href='here'>link</a><img src='there'/></body></html>"
    mocked_get.return_value.content = b"hello"
    with pytest.raises(ValueError, match="Unable to get header from file"):
        data, imgf = get_parse_data(outdir=tmp_path, get_img=True)
