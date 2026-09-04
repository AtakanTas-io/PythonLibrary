"""Hız testi modülü testleri."""

import sys
from unittest.mock import MagicMock, patch
import pytest

from python_library.speedtest_tool import run_speedtest
from python_library.exceptions import DependencyError


def test_speedtest_missing_dependency():
    with patch.dict(sys.modules, {"speedtest": None}):
        with pytest.raises(DependencyError, match="speedtest-cli"):
            run_speedtest()


def test_speedtest_success():
    mock_st_instance = MagicMock()
    mock_st_instance.results.dict.return_value = {
        "download": 100_000_000,  # 100 Mbps
        "upload": 50_000_000,     # 50 Mbps
        "ping": 12.5,
        "server": {"name": "Istanbul", "country": "Turkey", "sponsor": "Turkcell"},
        "client": {"ip": "1.2.3.4"},
    }

    mock_speedtest = MagicMock()
    mock_speedtest.Speedtest.return_value = mock_st_instance

    with patch.dict(sys.modules, {"speedtest": mock_speedtest}):
        res = run_speedtest()
        assert res["download_mbps"] == 100.0
        assert res["upload_mbps"] == 50.0
        assert res["ping_ms"] == 12.5
        assert "Istanbul" in res["server"]
