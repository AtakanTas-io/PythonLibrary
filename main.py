import schedule
import time
from plyer import notification

def su_icme_uyarisi():
    notification.notify(
        title = "Su İçme Vakti! 💧",
        message = "Sağlığın için bir bardak su içmeyi unutma. Hadi, hemen mutfağa!",
        app_name = "Su Hatırlatıcı",
        timeout = 15
    )
    print("Bildirim gönderildi: Su içme vakti!")


schedule.every(10).minutes.do(su_icme_uyarisi)



print("Su Hatirlaticisi aktif")

while True:
    schedule.run_pending()
    time.sleep(1)