from typer.testing import CliRunner
import sqlite3
import os
from cli_todo import __version__
from cli_todo.cli import cli
from cli_todo.cli import Db

runner = CliRunner()


def test_version():
    assert __version__ == '0.1.0'


def test_cli(monkeypatch):
    def get_db(self):
        return sqlite3.connect('/tmp/test.db')

    monkeypatch.setattr(Db, 'get_db', get_db)

    result = runner.invoke(cli, ['add', '--text', 'test todo'])
    assert result.exit_code == 0
    result = runner.invoke(cli, ['list'])
    assert result.exit_code == 0
    assert 'test todo' in result.stdout
    index = int(result.stdout.split(',')[0])
    result = runner.invoke(cli, ['remove', str(index)])
    assert result.exit_code == 0
    result = runner.invoke(cli, ['list'])
    assert 'test todo' not in result.stdout
    os.remove('/tmp/test.db')


def test_add():
    pass


def test_remove():
    pass


def test_remove_many():
    pass


def test_restore():
    pass


def test_done():
    pass


def test_undone():
    pass


def test_timer_start():
    pass


def test_timer_stop():
    pass


def test_chose_random():
    pass


def test_skip():
    pass


def test_skip_max():
    pass
