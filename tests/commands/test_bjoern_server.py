import pytest
try:
    import bjoern
except ImportError:
    pytestmark = pytest.mark.skip(reason="Unable to import bjoern")
else:
    import time
    import delegator
    import requests
    from .shared import TEST_APP, PROG


BJOERN_PARAMS = [
    ([], ""),
    (["--reuse=True"], ""),
    (["--bind=:8060"], "http://127.0.0.1:8060"),
    (["--bind=127.0.0.2"], "http://127.0.0.2:8000")
]


@pytest.mark.parametrize("cmd,conn", BJOERN_PARAMS)
def test_bjoern_server(cmd, conn):
    call = [PROG, "bjoern", TEST_APP]
    call.extend(cmd)
    srv = delegator.run(call, block=False)
    time.sleep(1)
    conn = conn or "http://127.0.0.1:8000"
    response = requests.get(conn, timeout=60)
    assert response.status_code == requests.codes.ok
    assert "Hello WEPPY!" in response.text
    srv.kill()
