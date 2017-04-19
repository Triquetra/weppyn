#!/usr/bin/env python

import click
import delegator


@click.group()
def cli():
    pass


@cli.command()
@click.argument('start_dir', nargs=1, required=False)
def test(start_dir):
    if not start_dir:
        start_dir = "/tmp/weppyn/"
    print("Starting pytest in", start_dir)
    import ipdb; ipdb.set_trace()
    delegator.run(["pytest", "--cov=weppyn", start_dir])


@cli.command()
@click.argument('server', nargs=1)
@click.argument('app', nargs=1, default='/home/weppy/sample_app.py')
@click.option('--bind', default='0.0.0.0:8000')
def run(server, app, bind):
    delegator.run(["weppyn", server, app, "--bind", bind])


if __name__ == "__main__":
    cli()
