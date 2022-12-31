from flask import Flask
from flask.typing import ResponseReturnValue, RouteCallable
from waitress import serve
import importlib.util
import os
import re

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
STATIC_DIR = os.path.join(PROJECT_DIR, 'static')
ROUTES_DIR = os.path.join(PROJECT_DIR, 'routes')
METHOD_NAMES = ['get', 'post', 'put', 'delete', 'patch', 'options', 'head']

app = Flask(__name__, static_folder=STATIC_DIR)

def route_to_uri(route):
    return route.replace(ROUTES_DIR, '')

def route_to_name(route):
    return re.sub(r'>?/<?', '_', route_to_uri(route))

def route_to_mod_name(route, type = 'index'):
    return 'routes' + route_to_name(route).replace('_', '.') + type

def route_to_index(route, file = 'index.py'):
    return os.path.join(route, file)

def route_to_mod(route, type = 'index'):
    index_file = route_to_index(route, type + '.py')
    spec = importlib.util.spec_from_file_location(route_to_mod_name(route, type), index_file)

    if spec is None or spec.loader is None:
        print('No spec found for {}'.format(index_file))
        return None 

    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    
    return mod

def mods_to_handlers(mods):
    handlers = []

    for mod in mods:
        if mod is not None and hasattr(mod, 'handler'):
            handlers.append(mod.handler)

    return handlers

def get_routes(startpath, type = 'index'):
    routes = dict()

    for root, _, files in os.walk(startpath):
        if type + '.py' in files:
            uri = root
            if not uri.endswith('/'):
                uri += '/'

            routes[uri] = route_to_mod(uri, type)

    return routes

def generate_handler(*args) -> RouteCallable:
    def _handler(**kwargs) -> ResponseReturnValue:
        for handler in args:
            return_value = handler(**kwargs)

            if return_value is not None:
                return return_value

        return "Internal Server Error", 500

    return _handler


def add_routes_to_app():
    middlewares = get_routes(ROUTES_DIR, 'middleware')
    routes = get_routes(ROUTES_DIR)

    for route, mod in routes.items():
        filtered_middlewares = dict(filter(lambda item: route.startswith(item[0]), middlewares.items()))

        for method_name in METHOD_NAMES:
            method = getattr(mod, method_name, None)

            if method is None:
                continue

            handler = generate_handler(*mods_to_handlers(filtered_middlewares.values()), method)

            app.add_url_rule(route_to_uri(route), route_to_name(route), handler, methods=[method_name.upper()])


    for rule in app.url_map.iter_rules():
        print('Found route:', rule, end=' -> ')
        print('with Methods', rule.methods)


def dev():
    add_routes_to_app()
    app.run(port=8000, debug=True, use_reloader=False)

def prod():
    add_routes_to_app()
    serve(app, host='0.0.0.0', port=8000)

if __name__ == '__main__':
    prod()
