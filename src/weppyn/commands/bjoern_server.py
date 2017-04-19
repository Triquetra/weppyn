import click


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
    try:
        import bjoern
    except ModuleNotFoundError:
        msg = "Please install bjoern ('pip install bjoern'), and try again."
        click.echo(msg)
    else:
        from weppyn.utilities import set_app_value
        app_exec = set_app_value(app)
        if bind.startswith('unix:'):
            bjoern.run(ctx.app_exec, bind)
        else:
            from weppyn.utilities import get_host_and_port
            app_exec = set_app_value(app)
            host, port = get_host_and_port(bind)
            bjoern.run(app_exec, host, port, reuse_port=reuse)
