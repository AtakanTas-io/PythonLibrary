"""Su İçme ve Masaüstü Hatırlatıcı Modülü."""

import time
import sys
from typing import Optional, Callable
from python_library.exceptions import DependencyError, ValidationError


def send_notification(
    title: str = "Su İçme Vakti! 💧",
    message: str = "Sağlığın için bir bardak su içmeyi unutma. Hadi, hemen mutfağa!",
    app_name: str = "Su Hatırlatıcı",
    timeout: int = 10,
) -> bool:
    """Masaüstü bildirimi gönderir.

    Args:
        title (str): Bildirim başlığı.
        message (str): Bildirim mesajı içeriği.
        app_name (str): Bildirimde görünecek uygulama adı.
        timeout (int): Bildirimin ekranda kalma süresi (saniye).

    Returns:
        bool: Bildirim başarıyla tetiklendiyse True döner.

    Raises:
        ValidationError: Parametreler geçersizse fırlatılır.
        DependencyError: 'plyer' kütüphanesi yüklü değilse fırlatılır.
    """
    if not title or not title.strip():
        raise ValidationError("Bildirim başlığı boş olamaz.")
    if not message or not message.strip():
        raise ValidationError("Bildirim mesajı boş olamaz.")
    if timeout <= 0:
        raise ValidationError("Bildirim süresi pozitif bir sayı olmalıdır.")

    try:
        from plyer import notification
    except ImportError as err:
        raise DependencyError(
            "Masaüstü bildirimleri için 'plyer' kütüphanesi gereklidir. "
            "Lütfen 'pip install plyer' komutunu çalıştırın."
        ) from err

    notification.notify(
        title=title,
        message=message,
        app_name=app_name,
        timeout=timeout,
    )
    return True


def start_reminder_loop(
    interval_minutes: int = 10,
    title: str = "Su İçme Vakti! 💧",
    message: str = "Sağlığın için bir bardak su içmeyi unutma. Hadi, hemen mutfağa!",
    app_name: str = "Su Hatırlatıcı",
    timeout: int = 10,
    max_runs: Optional[int] = None,
    on_notify: Optional[Callable[[], None]] = None,
) -> None:
    """Belirli aralıklarla su hatırlatıcı döngüsünü başlatır.

    Args:
        interval_minutes (int): Hatırlatma periyodu (dakika cinsinden).
        title (str): Bildirim başlığı.
        message (str): Bildirim mesajı.
        app_name (str): Uygulama adı.
        timeout (int): Bildirim süresi.
        max_runs (Optional[int]): Maksimum çalışma sayısı (test ve kontrollü çıkış için).
        on_notify (Optional[Callable]): Her bildirimde ek çalışacak callback fonksiyonu.

    Raises:
        ValidationError: interval_minutes <= 0 ise fırlatılır.
        DependencyError: 'schedule' kütüphanesi yüklü değilse fırlatılır.
    """
    if interval_minutes <= 0:
        raise ValidationError("Hatırlatma aralığı 0'dan büyük olmalıdır.")

    try:
        import schedule
    except ImportError as err:
        raise DependencyError(
            "Zamanlayıcı için 'schedule' kütüphanesi gereklidir. "
            "Lütfen 'pip install schedule' komutunu çalıştırın."
        ) from err

    def job():
        send_notification(title=title, message=message, app_name=app_name, timeout=timeout)
        if on_notify:
            on_notify()

    # Önceki kayıtlı job'ları temizle ve yeni job planla
    schedule.clear("water_reminder")
    schedule.every(interval_minutes).minutes.do(job).tag("water_reminder")

    print(f"[{app_name}] aktif edildi! Her {interval_minutes} dakikada bir bildirim gönderilecek. (Durdurmak için Ctrl+C)")

    run_count = 0
    try:
        while True:
            schedule.run_pending()
            if max_runs is not None:
                run_count += 1
                if run_count >= max_runs:
                    break
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nHatırlatıcı kullanıcı tarafından durduruldu.")
    finally:
        schedule.clear("water_reminder")
