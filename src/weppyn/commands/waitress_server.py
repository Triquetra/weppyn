import click
try:
    from waitress import serve
except ImportError:
    waitress_installed = False
else:
    waitress_installed = True
    from weppyn.utilities import set_app_value, num_workers


@click.command('waitress', short_help='pure python WSGI server')
@click.argument('app', nargs=1, required=False)
@click.option('--bind', default='0.0.0.0:8080', show_default=True,
              help='HOST, HOST:PORT, :PORT, unix:/path/to/socket')
@click.option('--threads', default='4', show_default=True,
              help='number of threads used to process application logic')
@click.pass_context
def cli(ctx, app, bind, threads):
    if not app:
        print(ctx.get_help())
        exit()
    if waitress_installed:
        app_exec = set_app_value(app)
        threads = num_workers(threads)
        if bind.startswith('unix:'):
            serve(app_exec, unix_socket=bind[5:], threads=threads)
        else:
            from weppyn.utilities import get_host_and_port
            host, port = get_host_and_port(bind)
            serve(app_exec, host=host, port=port, threads=threads)
    else:
        click.echo("Unable to import waitress.  Please install waitress and try again.")
