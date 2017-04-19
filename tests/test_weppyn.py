"""Testing weppyn.cli."""
import os
import delegator
import pytest
from weppyn.cli import PLUGIN_FOLDER
from .commands.shared import PROG


CMD = [cmd[:-10] for cmd in os.listdir(PLUGIN_FOLDER)
       if cmd.endswith('_server.py')]


def test_weppyn():
    """Test weppyn.cli.cli."""
    cmd = delegator.run(PROG)
    assert cmd.return_code == 0
    assert "A unified server interface for weppy applications." in cmd.out


@pytest.mark.parametrize("command", CMD)
def test_commands(command):
    """Test weppyn commands."""
    cmd = delegator.run([PROG, command])
    assert cmd.return_code == 0
