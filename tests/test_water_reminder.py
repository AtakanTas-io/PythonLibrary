"""Su Hatırlatıcı modülü testleri."""

import sys
from unittest.mock import MagicMock, patch
import pytest

from python_library.water_reminder import send_notification, start_reminder_loop
from python_library.exceptions import ValidationError, DependencyError


def test_send_notification_validation():
    with pytest.raises(ValidationError, match="başlığı boş olamaz"):
        send_notification(title="")

    with pytest.raises(ValidationError, match="mesajı boş olamaz"):
        send_notification(title="Başlık", message="")

    with pytest.raises(ValidationError, match="pozitif bir sayı"):
        send_notification(title="Başlık", message="Mesaj", timeout=0)


def test_send_notification_missing_dependency():
    with patch.dict(sys.modules, {"plyer": None}):
        with pytest.raises(DependencyError, match="plyer"):
            send_notification(title="Test", message="Test Mesaj")


def test_send_notification_success():
    mock_notification = MagicMock()
    mock_plyer = MagicMock()
    mock_plyer.notification = mock_notification

    with patch.dict(sys.modules, {"plyer": mock_plyer}):
        result = send_notification(
            title="Su Vakti",
            message="Su için",
            app_name="App",
            timeout=5,
        )
        assert result is True
        mock_notification.notify.assert_called_once_with(
            title="Su Vakti",
            message="Su için",
            app_name="App",
            timeout=5,
        )


def test_start_reminder_loop_invalid_interval():
    with pytest.raises(ValidationError, match="0'dan büyük olmalıdır"):
        start_reminder_loop(interval_minutes=0)


def test_start_reminder_loop_missing_dependency():
    with patch.dict(sys.modules, {"schedule": None}):
        with pytest.raises(DependencyError, match="schedule"):
            start_reminder_loop(interval_minutes=5)


def test_start_reminder_loop_controlled_run():
    mock_schedule = MagicMock()
    mock_job = MagicMock()
    mock_schedule.every.return_value.minutes.do.return_value.tag.return_value = mock_job

    called = []
    def on_notify_callback():
        called.append(True)

    with patch.dict(sys.modules, {"schedule": mock_schedule}):
        start_reminder_loop(
            interval_minutes=15,
            max_runs=2,
            on_notify=on_notify_callback,
        )

        mock_schedule.clear.assert_called()
        mock_schedule.every.assert_called_once_with(15)
        assert mock_schedule.run_pending.call_count == 2
