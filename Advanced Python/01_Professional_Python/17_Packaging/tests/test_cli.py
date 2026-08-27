from __future__ import annotations

from bioseqkit.cli import main


def test_cli_prints_summary_for_valid_sequence(capsys) -> None:  # noqa: ANN001
    exit_code = main(["ACGT"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "length=4" in captured.out


def test_cli_returns_error_code_for_invalid_sequence(capsys) -> None:  # noqa: ANN001
    exit_code = main(["ACGTX"])
    captured = capsys.readouterr()
    assert exit_code == 1
    assert "error" in captured.err


def test_cli_version_flag(capsys) -> None:  # noqa: ANN001
    exit_code = main(["--version"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out.strip()
