"""Test Suite for weppy_serve.utilities."""

import multiprocessing
import os.path
import pytest
import sys
from weppy import App
import weppyn.utilities as util

NUM_WORKERS_DATA = [
    ("4", 4),
    ("0", 1),
    ("-1", 1),
    ("5/2", 2),
    ("11/3", 3),
    ("X", multiprocessing.cpu_count()),
    ("X*2+1", multiprocessing.cpu_count() * 2 + 1),
    ("(X*4)/2", (multiprocessing.cpu_count() * 4) / 2),
    ("x*2-1", multiprocessing.cpu_count() * 2 - 1)
]


@pytest.mark.parametrize("formula,expected", NUM_WORKERS_DATA)
def test_num_workers(formula, expected):
    """Test weppyn.utilities.num_workers."""
    assert util.num_workers(formula) == expected


BAD_FORMULA_DATA = [
    ("2.9"),
    ("2,9"),
    ("bad formula")
]


@pytest.mark.parametrize("formula", BAD_FORMULA_DATA)
def test_num_workers_exception(formula):
    """Test exception for bad expression."""
    with pytest.raises(SyntaxError):
        util.num_workers(formula)


GET_HOST_AND_PORT_DATA = [
    ("192.168.1.1", ("192.168.1.1", 8000)),
    ("192.168.1.1:8181", ("192.168.1.1", 8181)),
    (":8181", ("127.0.0.1", 8181))
]


@pytest.mark.parametrize("connection,expected", GET_HOST_AND_PORT_DATA)
def test_get_host_and_port(connection, expected):
    """Test weppyn.utilities.get_host_and_port."""
    assert util.get_host_and_port(connection) == expected


TEST_APP = os.path.join(os.path.dirname(__file__), "commands/sample_app.py")


def test_set_app_value():
    mod_path = util.prepare_exec_for_file(TEST_APP)
    assert mod_path == "tests.commands.sample_app"
    assert isinstance(util.locate_app(mod_path), App)
    mod_and_obj = util.get_app_module(mod_path)
    assert mod_and_obj == (mod_path, sys.modules.get(mod_path), None)
    assert isinstance(util.find_best_app(sys.modules.get(mod_path)), App)
    assert isinstance(util.set_app_value(TEST_APP), App)
