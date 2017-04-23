import os.path
import pytest
try:
    from pulsar.apps import wsgi
except ImportError:
    pytestmark = pytest.mark.skip(reason="Unable to import Pulsar")
try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock
from click.testing import CliRunner
from weppyn.cli import cli as weppyn
from .shared import TEST_APP


pytestmark = pytest.mark.skip(reason="Pulsar < 2.0 is incompatible with click")


@pytest.fixture
def mock_wsgi():
    wsgi = Mock(wsgi)
    return wsgi


PULSAR_SERVER_DATA = [
    (['pulsar'], 1, "Interface to the Pulsar asyncio framework"),
    (['pulsar', TEST_APP], 0, "")
]


@pytest.mark.parametrize("args,code,output", PULSAR_SERVER_DATA)
def test_pulsar_server(args, code, output):
    runner = CliRunner()
    result = runner.invoke(weppyn, args)
    assert result.exit_code == code
    assert output in result.output
