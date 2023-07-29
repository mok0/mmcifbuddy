from mmcifreader.convert import is_int, is_float, is_version


def test_int() -> None:
    """Pytest function to test int conversion"""
    assert is_int ("7.6") == None
    assert is_int("7") == 7
    assert is_int("7.") == None
    assert is_int(".6") == None
    assert is_int("-7.6") == None
    assert is_int("-7") == -7
    assert is_int("-7.") == None
    assert is_int("-.6") == None
    assert is_int("10007.61111") == None
    assert is_int("10007") == 10007
    assert is_int("10007.") == None
    assert is_int(".6100007") == None
    assert is_int("-72222.6") == None
    assert is_int("-7222") == -7222
    assert is_int("-74444.") == None
    assert is_int("-.63453") == None
    assert is_int("0") == 0
    assert is_int("0.0") == None
    assert is_int("1.0e6") == None
    assert is_int("-1.0e6") == None
    assert is_int("2.0e-3") == None
    assert is_int("-2.0e-3") == None
    assert is_int("10.11.") == None

def test_int() -> None:
    """Pytest function to test float conversion"""
    assert is_float ("7.6") == 7.6
    assert is_float("7") == None
    assert is_float("7.") == 7.0
    assert is_float("0.6") == 0.6
    assert is_float(".6") == 0.6
    assert is_float("-7.6") == -7.6
    assert is_float("-7") == None
    assert is_float("-7.") == -7.0
    assert is_float("-.6") == -0.6
    assert is_float("10007.61111") == 10007.61111
    assert is_float("10007") == None
    assert is_float("10007.") == 10007.0
    assert is_float("0.6100007") == 0.6100007
    assert is_float("-72222.6") == -72222.6
    assert is_float("-7222") == None
    assert is_float("-74444.") == -74444.
    assert is_float("-0.63453") == -.63453
    assert is_float("0") == None
    assert is_float("0.0") == 0.0
    assert is_float("1.0e6") == 1000000.0
    assert is_float("-1.0e6") == -1000000.0
    assert is_float("2.0e-3") == 0.002
    assert is_float("-2.0e-3") == -0.002
    assert is_float("2.7.8.37") == None
    assert is_float("10.11.") == None
    assert is_float(".") == None

def test_version() -> None:

    assert is_version("10.11.") == True
    assert is_version("100.222.333") == True
    assert is_version("10.11.1") == True
    assert is_version("10.11.1.5") == True
    assert is_version("10.1") == False
    assert is_version("10.10.") == True