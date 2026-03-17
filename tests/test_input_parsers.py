import pytest

from app.utils.input_parsers import parse_float, parse_int


def test_parse_int_ok():
    assert parse_int('10', 'nivel', required=True) == 10


def test_parse_int_invalid_raises():
    with pytest.raises(ValueError):
        parse_int('abc', 'nivel', required=True)


def test_parse_float_with_minimum():
    with pytest.raises(ValueError):
        parse_float('-1', 'costo', required=True, minimum=0)
