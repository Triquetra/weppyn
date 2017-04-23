import click
try:
    from meinheld import server
except ImportError:
    meinheld_installed = False
else:
    from meinheld import patch as monkeypatch
    from weppyn.utilities import set_app_value, get_host_and_port
    meinheld_installed = True


@click.command('meinheld', short_help='picoev and greenlet based high-performance server')
@click.argument('app', nargs=1, required=False)
@click.option('--bind', default='127.0.0.1:8000', show_default=True,
              help='HOST, HOST:PORT, :PORT')
@click.option('--nopatch', type=bool, default=False, show_default=True,
              help="do not monkeypatch the socket module")
@click.pass_context
def cli(ctx, app, bind, nopatch):
    """Interface to the Meinheld high-performance wsgi server.

    APP may be either an absolute or a relative path to the module
    containing the app to be served.  The app instance may also be
    specified after a colon:  "path/to/module:app"
    """
    if not app:
        print(ctx.get_help())
        exit()
    if meinheld_installed:
        if not nopatch:
            monkeypatch.patch_all()
        server.listen(get_host_and_port(bind))
        server.run(set_app_value(app))
    else:
        click.echo("Unable to import Meinheld.  Please install Meinheld and try again")
