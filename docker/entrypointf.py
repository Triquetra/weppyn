#!/usr/bin/env python
"""Experimental rewrite of entrypoint.py using fire."""

import fire
import delegator


def cli():
    fire.Fire({'test': test, 'run': run})


def test(start_dir="/tmp/weppyn/"):
    delegator.run(["pytest", start_dir])


def run(server, app="/home/weppy/sample_app.py", bind="127.0.0.1:8000"):
    delegator.run(["weppyn", server, app, "--bind", bind])


if __name__ == "__main__":
    cli()
