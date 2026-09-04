"""Ağ, Dış IP, DNS ve Port Tarama Araçları Modülü."""

import socket
from typing import Any, Dict, List
from python_library.exceptions import DependencyError, ValidationError, ConversionError


def get_network_info() -> Dict[str, Any]:
    """Cihazın dış IP adresini, konumunu ve ISP bilgilerini getirir."""
    try:
        import requests
    except ImportError as err:
        raise DependencyError("Ağ sorgulaması için 'requests' gereklidir.") from err

    try:
        # Güvenilir ve ücretsiz ip-api servisi
        res = requests.get("http://ip-api.com/json/", timeout=8)
        res.raise_for_status()
        data = res.json()
        if data.get("status") != "success":
            raise ConversionError(f"IP sorgulanamadı: {data.get('message', 'Bilinmeyen hata')}")

        return {
            "public_ip": data.get("query", ""),
            "country": data.get("country", ""),
            "city": data.get("city", ""),
            "isp": data.get("isp", ""),
            "timezone": data.get("timezone", ""),
        }
    except Exception as e:
        raise ConversionError(f"Ağ bilgileri alınırken hata oluştu: {e}") from e


def scan_ports(
    host: str = "localhost",
    ports: List[int] = None,
    timeout: float = 0.5,
) -> Dict[int, str]:
    """Hedef sunucudaki belirtilen portların açık olup olmadığını kontrol eder."""
    if not host or not host.strip():
        raise ValidationError("Hedef ana makine (host) boş olamaz.")

    check_ports = ports or [21, 22, 25, 53, 80, 110, 143, 443, 3306, 3389, 5432, 8080]
    results = {}

    for port in check_ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            status = sock.connect_ex((host.strip(), port))
            results[port] = "AÇIK" if status == 0 else "KAPALI"

    return results


def dns_lookup(domain: str, record_types: List[str] = None) -> Dict[str, List[str]]:
    """Belirtilen alan adı için DNS kayıtlarını (A, MX, TXT, NS vb.) sorgular."""
    if not domain or not domain.strip():
        raise ValidationError("Alan adı (domain) boş olamaz.")

    try:
        import dns.resolver
    except ImportError as err:
        raise DependencyError("DNS işlemleri için 'dnspython' gereklidir.") from err

    clean_domain = domain.strip().replace("http://", "").replace("https://", "").split("/")[0]
    types = record_types or ["A", "MX", "TXT", "NS"]
    records: Dict[str, List[str]] = {}

    for r_type in types:
        try:
            answers = dns.resolver.resolve(clean_domain, r_type)
            records[r_type] = [str(r.to_text()) for r in answers]
        except Exception:
            records[r_type] = []

    return records
