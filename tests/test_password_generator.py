"""Parola üretici testleri."""

import pytest
from python_library.password_generator import generate_password, check_password_strength
from python_library.exceptions import ValidationError


def test_generate_password_length():
    pwd = generate_password(length=20)
    assert len(pwd) == 20

    pwd_short = generate_password(length=8)
    assert len(pwd_short) == 8


def test_generate_password_too_short():
    with pytest.raises(ValidationError, match="en az 6 karakter"):
        generate_password(length=4)


def test_generate_password_no_charset():
    with pytest.raises(ValidationError, match="En az bir karakter türü"):
        generate_password(use_upper=False, use_lower=False, use_digits=False, use_special=False)


def test_check_password_strength():
    weak = check_password_strength("123")
    assert weak["score"] <= 2

    strong = check_password_strength("K9#mQ!z99$LpW@x8")
    assert strong["score"] >= 4
    assert strong["entropy"] > 60

    empty = check_password_strength("")
    assert empty["score"] == 0
