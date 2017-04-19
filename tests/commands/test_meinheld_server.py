import time
import delegator
import requests
import pytest
try:
    from meinheld import server
except ImportError:
    pytestmark = pytest.mark.skip(reason="Unable to import Meinheld")
from .shared import TEST_APP, PROG


MEINHELD_PARAMS = [
    [PROG, "meinheld", TEST_APP],
    [PROG, "meinheld", "--bind=False", TEST_APP],
    [PROG, "meinheld", ]
]


@pytest.fixture(scope="module")
def myserver():
    cmd = delegator.run([PROG, "meinheld", TEST_APP, "--bind=0.0.0.0"], block=False)
    time.sleep(0.1)
    yield cmd
    cmd.kill()


def test_meinheld_server(myserver):
    response = requests.get("http://127.0.0.1:8000", timeout=60)
    assert response.status_code == requests.codes.ok
    assert "Hello WEPPY!" in response.text
