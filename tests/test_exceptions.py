"""İstisna sınıflarının hiyerarşi ve mesaj testleri."""

import pytest
from python_library.exceptions import (
    PythonLibraryError,
    ValidationError,
    DependencyError,
    ConversionError,
)


def test_exception_hierarchy():
    assert issubclass(ValidationError, PythonLibraryError)
    assert issubclass(DependencyError, PythonLibraryError)
    assert issubclass(ConversionError, PythonLibraryError)


def test_exception_messages():
    err = ValidationError("Girdi geçersiz!")
    assert str(err) == "Girdi geçersiz!"
    assert isinstance(err, Exception)
