import click


@click.command('pulsar', short_help='multiprocessing asyncio wsgi server')
@click.argument('app', nargs=1, required=False)
@click.option('--bind', default='127.0.0.1:8060', show_default=True,
              help='HOST, HOST:PORT, :PORT, unix:/path/to/socket')
@click.option('--config', help="/path/to/config.py")
@click.option('--reload', type=bool, default=False, show_default=True,
              help="Auto reload modules when changes occur")
@click.option('--threads', default=5, show_default=True,
              help='number of threads used by the actor event loop executor')
@click.option('--workers', default="2", show_default=True,
              help='number of workers for handling requests')
@click.pass_context
def cli(ctx, app, bind, config, reload, threads, workers):
    """Interface to the Pulsar asyncio framework's wsgi server.

    APP may be either an absolute or a relative path to the module
    containing the app to be served.  The app instance may also be
    specified after a colon:  "path/to/module:app"

    Currently not working because Pulsar <2.0 tries to pickle the callable,
    which includes click, which is not pickleable.
    """
    if not app:
        print(ctx.get_help())
        exit()
    try:
        from pulsar.apps import wsgi
    except ModuleNotFoundError:
        click.echo("Please install pulsar and try again.")
    else:
        try:
            from pulsar.apps.greenio import GreenPool, GreenWSGI
        except ModuleNotFoundError:
            msg = "Unable to load GreenWSGI.  Proceeding without greenlets."
            click.echo(msg)
            green_pulsar = False
        else:
            green_pulsar = True
            green_pool = GreenPool(max_workers=None, loop=None)

        from weppyn.utilities import set_app_value
        app_exec = set_app_value(app)

        if green_pulsar:
            class Site(wsgi.LazyWsgi):

                def setup(self, environ=None):
                    handler = GreenWSGI(app_exec, green_pool)
                    return handler
        else:
            class Site(wsgi.LazyWsgi):

                def setup(self, environ=None):
                    mwie = wsgi.middleware_in_executor(app_exec)
                    midware = [wsgi.wait_for_body_middleware, mwie]
                    handler = wsgi.WsgiHandler(midware)
                    return handler

        from weppyn.utilities import num_workers
        workers = num_workers(workers)

        # hack to prevent passing click arguments to pulsar
        import sys
        sys.argv = sys.argv[0:1]
        import ipdb; ipdb.set_trace()
        server = wsgi.WSGIServer(callable=Site(), bind=bind, config=config,
                                 reload=reload, thread_workers=threads,
                                 workers=workers)
        server.start()
