"""URL kısaltıcı testleri."""

from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest

from python_library.url_shortener import shorten_url, shorten_and_qr
from python_library.exceptions import ValidationError


def test_shorten_url_validation():
    with pytest.raises(ValidationError, match="boş olamaz"):
        shorten_url("")


@patch("requests.get")
def test_shorten_url_success(mock_get):
    mock_resp = MagicMock()
    mock_resp.text = "https://tinyurl.com/abc1234"
    mock_resp.status_code = 200
    mock_get.return_value = mock_resp

    res = shorten_url("https://example.com/very/long/url")
    assert res == "https://tinyurl.com/abc1234"
    mock_get.assert_called_once()


@patch("python_library.url_shortener.shorten_url")
@patch("python_library.url_shortener.generate_qr")
def test_shorten_and_qr(mock_gen_qr, mock_shorten, tmp_path: Path):
    mock_shorten.return_value = "https://tinyurl.com/test"
    mock_gen_qr.return_value = tmp_path / "test_qr.svg"

    link, qr = shorten_and_qr("https://google.com", qr_output=tmp_path / "test_qr.svg")
    assert link == "https://tinyurl.com/test"
    assert qr == tmp_path / "test_qr.svg"
    mock_shorten.assert_called_once_with("https://google.com")
    mock_gen_qr.assert_called_once_with("https://tinyurl.com/test", output_path=tmp_path / "test_qr.svg", scale=5)
