import click
try:
    import bjoern
except ModuleNotFoundError:
    bjoern_installed = False
else:
    bjoern_installed = True
    from weppyn.utilities import set_app_value


@click.command('bjoern', short_help='small, fast, lightweight')
@click.argument('app', nargs=1, required=False)
@click.option('--bind', default='127.0.0.1:8000', show_default=True,
              help='HOST, HOST:PORT, :PORT, unix:@socket_name, unix:/path/to/socket')
@click.option('--reuse', type=bool, default=False, show_default=True,
              help='enable SO_REUSEPORT if available')
@click.pass_context
def cli(ctx, app, bind, reuse):
    if not app:
        print(ctx.get_help())
        exit()
    if bjoern_installed:
        app_exec = set_app_value(app)
        if bind.startswith('unix:'):
            bjoern.run(app_exec, bind)
        else:
            from weppyn.utilities import get_host_and_port
            host, port = get_host_and_port(bind)
            bjoern.run(app_exec, host, port, reuse_port=reuse)
    else:
        click.echo("Unable to import bjoern.  Please install bjoern and try again.")
