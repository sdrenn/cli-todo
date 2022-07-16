from typer.testing import CliRunner
from cli_todo import __version__
from cli_todo.cli import cli

runner = CliRunner()


def test_version():
    assert __version__ == '0.1.0'


def test_cli():
    result = runner.invoke(cli, ['add', '--text', 'test todo'])
    assert result.exit_code == 0
    result = runner.invoke(cli, ['list'])
    assert result.exit_code == 0
    assert 'test todo' in result.stdout
    index = int(result.stdout.split(',')[0])
    result = runner.invoke(cli, ['remove', index])
    assert result.exit_code == 0
    result = runner.invoke(cli, ['list'])
    assert 'test todo' not in result.stdout
