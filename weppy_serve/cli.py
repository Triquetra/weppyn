"""
    serveweppy.cli
    ---------
    Provide a unified server launcher for weppy applications.
    :copyright: (c) 2017 by David Crandall
    Based on the code of weppy.cli (http://weppy.org)
    :copyright: (c) 2014-2017 by Giovanni Barillari.
    :license: BSD, see LICENSE for more details.
"""
import click
import os


plugin_folder = os.path.join(os.path.dirname(__file__), 'commands')


class SWCLI(click.MultiCommand):

    def list_commands(self, ctx):
        rv = [cmd[:-10] for cmd in os.listdir(plugin_folder)
              if cmd.endswith('_server.py')]
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        ns = {}
        fn = os.path.join(plugin_folder, name + '_server.py')
        with open(fn) as f:
            code = compile(f.read(), fn, 'exec')
            eval(code, ns, ns)
        return ns['cli']


@click.command(cls=SWCLI)
@click.pass_context
def cli(ctx):
    pass
