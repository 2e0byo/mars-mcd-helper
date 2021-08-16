from mars_mcd_helper.get_mars_data import generate_fn


def test_generate_fn():
    assert generate_fn(var1="this", var2="that") == "marsdata_this-that.txt"
