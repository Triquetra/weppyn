"""
weppyn.cli.

Provide a unified server launcher for weppy applications.
:copyright: (c) 2017 by David Crandall
Based on the code of weppy.cli (http://weppy.org)
:copyright: (c) 2014-2017 by Giovanni Barillari.
:license: BSD, see LICENSE for more details.
"""
import os
import click


PLUGIN_FOLDER = os.path.join(os.path.dirname(__file__), 'commands')


class _SWCLI(click.MultiCommand):

    def list_commands(self, ctx):
        rv = [cmd[:-10] for cmd in os.listdir(PLUGIN_FOLDER)
              if cmd.endswith('_server.py')]
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        ns = {}
        fn = os.path.join(PLUGIN_FOLDER, name + '_server.py')
        with open(fn) as f:
            code = compile(f.read(), fn, 'exec')
            eval(code, ns, ns)
        return ns['cli']


@click.command(cls=_SWCLI)
def cli():
    """A unified server interface for weppy applications.

    Note that each of the commands invokes a different server that has
    its own requirments which must be installed separately.
    """
    pass


if __name__ == "__main__":
    cli()
