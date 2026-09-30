import pytest

from frieren_nlp import __version__
from frieren_nlp.cli import main


def test_package_has_version():
    assert __version__ == "0.1.0"


def test_cli_without_stage_prints_help(capsys):
    assert main([]) == 0
    assert "usage: frieren" in capsys.readouterr().out


def test_cli_version_flag(capsys):
    with pytest.raises(SystemExit) as exit_info:
        main(["--version"])
    assert exit_info.value.code == 0
    assert __version__ in capsys.readouterr().out
