import multiprocessing
import os
import sys


def get_app_module(app_id):
    if ':' in app_id:
        module, app_obj = app_id.split(':', 1)
    else:
        module = app_id
        app_obj = None
    mod = sys.modules.get(module)
    if mod is None:
        __import__(module)
        mod = sys.modules[module]
    return module, mod, app_obj


def find_best_app(module):
    """Given a module instance this tries to find the best possible
    application in the module or raises an exception.
    """
    from weppy import App
    from weppy._compat import iteritems

    # Search for the most common names first.
    for attr_name in 'app', 'application':
        app = getattr(module, attr_name, None)
        if app is not None and isinstance(app, App):
            return app

    # Otherwise find the only object that is a weppy App instance.
    matches = [v for k, v in iteritems(module.__dict__) if isinstance(v, App)]

    if len(matches) == 1:
        return matches[0]
    raise Exception(
        'Failed to find application in module "%s".' % module.__name__
    )


def locate_app(app_id):
    """Attempt to locate the application."""
    module, mod, app_obj = get_app_module(app_id)
    if app_obj is None:
        app = find_best_app(mod)
    else:
        app = getattr(mod, app_obj, None)
        if app is None:
            raise RuntimeError('Failed to find application in module "%s"'
                               % module)
    return app


def prepare_exec_for_file(filename):
    """Given a filename this will try to calculate the python path, add it
    to the search path and return the actual module name that is expected.
    """
    module = []

    # Chop off file extensions or package markers
    if filename.endswith('.py'):
        filename = filename[:-3]
    elif os.path.split(filename)[1] == '__init__.py':
        filename = os.path.dirname(filename)
    else:
        raise Exception(
            'The file provided (%s) is not a valid Python file.')
    filename = os.path.realpath(filename)

    dirpath = filename
    while 1:
        dirpath, extra = os.path.split(dirpath)
        module.append(extra)
        if not os.path.isfile(os.path.join(dirpath, '__init__.py')):
            break

    sys.path.insert(0, dirpath)
    return '.'.join(module[::-1])


def set_app_value(value):
    if value is not None:
        if os.path.isfile(value):
            value = prepare_exec_for_file(value)
        elif '.' not in sys.path:
            sys.path.insert(0, '.')
    app = locate_app(value)
    return app


def num_workers(formula):
    """Calculate number of workers for multiprocessing."""
    if "X" in formula:
        workers = multiprocessing.cpu_count() * 2
    return workers


def get_host_and_port(connection):
    if connection.startswith(':'):
        host = '127.0.0.1'
        port = connection[1:]
    elif ':' in connection:
        host, port = connection.split(':', 1)
    else:
        host = connection
        port = '8000'
    return host, port
