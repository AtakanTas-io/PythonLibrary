"""Ağ araçları testleri."""

from unittest.mock import MagicMock, patch
import pytest

from python_library.network_tools import get_network_info, scan_ports, dns_lookup
from python_library.exceptions import ValidationError


@patch("requests.get")
def test_get_network_info(mock_get):
    mock_resp = MagicMock()
    mock_resp.json.return_value = {
        "status": "success",
        "query": "88.240.10.20",
        "country": "Turkey",
        "city": "Istanbul",
        "isp": "Turk Telekom",
        "timezone": "Europe/Istanbul",
    }
    mock_resp.status_code = 200
    mock_get.return_value = mock_resp

    info = get_network_info()
    assert info["public_ip"] == "88.240.10.20"
    assert info["city"] == "Istanbul"


@patch("socket.socket")
def test_scan_ports(mock_sock_cls):
    mock_sock = MagicMock()
    mock_sock.connect_ex.side_effect = lambda addr: 0 if addr[1] == 80 else 111
    mock_sock_cls.return_value.__enter__.return_value = mock_sock

    results = scan_ports("127.0.0.1", ports=[80, 443])
    assert results[80] == "AÇIK"
    assert results[443] == "KAPALI"


def test_scan_ports_validation():
    with pytest.raises(ValidationError, match="boş olamaz"):
        scan_ports("")


def test_dns_lookup_validation():
    with pytest.raises(ValidationError, match="boş olamaz"):
        dns_lookup("")


@patch("dns.resolver.resolve")
def test_dns_lookup_success(mock_resolve):
    mock_record = MagicMock()
    mock_record.to_text.return_value = "93.184.216.34"
    mock_resolve.return_value = [mock_record]

    res = dns_lookup("example.com", record_types=["A"])
    assert "A" in res
    assert res["A"] == ["93.184.216.34"]
