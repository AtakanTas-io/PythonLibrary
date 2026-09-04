"""CLI komut satırı arayüzü testleri."""

from unittest.mock import MagicMock, patch
import pytest

from python_library.cli import main, build_parser, interactive_menu
from python_library.exceptions import ValidationError


def test_cli_parser_qr_args():
    parser = build_parser()
    args = parser.parse_args(["qr", "https://test.com", "-o", "out.svg", "-s", "7", "-f", "svg"])
    assert args.command == "qr"
    assert args.content == "https://test.com"
    assert args.output == "out.svg"
    assert args.scale == 7
    assert args.format == "svg"


def test_cli_parser_pdf_args():
    parser = build_parser()
    args = parser.parse_args(["pdf", "doc.pdf", "-o", "out.docx"])
    assert args.command == "pdf"
    assert args.pdf_path == "doc.pdf"
    assert args.output == "out.docx"


def test_cli_parser_bg_args():
    parser = build_parser()
    args = parser.parse_args(["remove-bg", "photo.jpg", "-o", "clean.png"])
    assert args.command == "remove-bg"
    assert args.image_path == "photo.jpg"
    assert args.output == "clean.png"


def test_cli_parser_reminder_args():
    parser = build_parser()
    args = parser.parse_args(["reminder", "-i", "20", "-t", "Su", "-m", "İç"])
    assert args.command == "reminder"
    assert args.interval == 20
    assert args.title == "Su"
    assert args.message == "İç"


@patch("python_library.cli.generate_qr")
def test_cli_run_qr_success(mock_generate_qr):
    mock_generate_qr.return_value = "qrcode.svg"
    exit_code = main(["qr", "https://example.com"])
    assert exit_code == 0
    mock_generate_qr.assert_called_once()


@patch("python_library.cli.convert_pdf_to_docx")
def test_cli_run_pdf_success(mock_convert):
    mock_convert.return_value = "doc.docx"
    exit_code = main(["pdf", "sample.pdf"])
    assert exit_code == 0
    mock_convert.assert_called_once()


@patch("python_library.cli.remove_background")
def test_cli_run_bg_success(mock_remove_bg):
    mock_remove_bg.return_value = "out.png"
    exit_code = main(["remove-bg", "image.jpg"])
    assert exit_code == 0
    mock_remove_bg.assert_called_once()


@patch("python_library.cli.start_reminder_loop")
def test_cli_run_reminder_success(mock_reminder):
    exit_code = main(["reminder", "-i", "5", "-t", "Başlık", "-m", "Mesaj"])
    assert exit_code == 0
    mock_reminder.assert_called_once_with(
        interval_minutes=5,
        title="Başlık",
        message="Mesaj",
    )


@patch("python_library.cli.generate_qr")
def test_cli_handles_validation_error(mock_generate_qr):
    mock_generate_qr.side_effect = ValidationError("Hatalı parametre")
    exit_code = main(["qr", "invalid"])
    assert exit_code == 1


@patch("python_library.cli.generate_qr")
def test_cli_handles_unexpected_error(mock_generate_qr):
    mock_generate_qr.side_effect = RuntimeError("Bilinmeyen hata")
    exit_code = main(["qr", "test"])
    assert exit_code == 2


@patch("builtins.input", side_effect=["0"])
def test_cli_interactive_exit(mock_input):
    exit_code = main([])
    assert exit_code == 0


@patch("builtins.input", side_effect=[KeyboardInterrupt])
def test_cli_interactive_keyboard_interrupt(mock_input):
    exit_code = main([])
    assert exit_code == 1


@patch("builtins.input", side_effect=["99"])
def test_interactive_menu_invalid(mock_input, capsys):
    interactive_menu()
    captured = capsys.readouterr()
    assert "Geçersiz seçim!" in captured.out


@patch("python_library.cli.generate_qr")
@patch("builtins.input", side_effect=["5", "https://test.com"])
def test_interactive_menu_qr(mock_input, mock_qr):
    mock_qr.return_value = "qrcode.svg"
    interactive_menu()
    mock_qr.assert_called_once_with("https://test.com")


@patch("python_library.cli.convert_pdf_to_docx")
@patch("builtins.input", side_effect=["1", "test.pdf"])
def test_interactive_menu_pdf(mock_input, mock_pdf):
    mock_pdf.return_value = "test.docx"
    interactive_menu()
    mock_pdf.assert_called_once_with("test.pdf")


@patch("python_library.cli.remove_background")
@patch("builtins.input", side_effect=["6", "test.jpg"])
def test_interactive_menu_bg(mock_input, mock_bg):
    mock_bg.return_value = "test_no_bg.png"
    interactive_menu()
    mock_bg.assert_called_once_with("test.jpg")


@patch("python_library.cli.start_reminder_loop")
@patch("builtins.input", side_effect=["15"])
def test_interactive_menu_reminder(mock_input, mock_rem):
    interactive_menu()
    mock_rem.assert_called_once_with(interval_minutes=15)
