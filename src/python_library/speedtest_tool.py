"""İnternet Hız Testi (Download, Upload, Ping) Modülü."""

from typing import Any, Dict
from python_library.exceptions import DependencyError, ConversionError


def run_speedtest() -> Dict[str, Any]:
    """İnternet bağlantı hızını (indirme, yükleme ve gecikme) test eder."""
    try:
        import speedtest
    except ImportError as err:
        raise DependencyError(
            "Hız testi için 'speedtest-cli' kütüphanesi gereklidir. "
            "Lütfen 'pip install speedtest-cli' çalıştırın."
        ) from err

    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        st.download()
        st.upload()
        results = st.results.dict()

        download_mbps = round(results.get("download", 0) / 1_000_000, 2)
        upload_mbps = round(results.get("upload", 0) / 1_000_000, 2)
        ping_ms = round(results.get("ping", 0), 2)
        server_info = results.get("server", {})

        return {
            "download_mbps": download_mbps,
            "upload_mbps": upload_mbps,
            "ping_ms": ping_ms,
            "server": f"{server_info.get('name', '')} ({server_info.get('country', '')})",
            "sponsor": server_info.get("sponsor", ""),
            "client_ip": results.get("client", {}).get("ip", ""),
        }
    except Exception as e:
        raise ConversionError(f"Hız testi yapılırken hata oluştu: {e}") from e
