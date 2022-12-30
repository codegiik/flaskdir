from flask import Flask
from waitress import serve
import importlib.util
import os
import re

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
STATIC_DIR = os.path.join(PROJECT_DIR, 'static')
ROUTES_DIR = os.path.join(PROJECT_DIR, 'routes')
METHOD_NAMES = ['get', 'post', 'put', 'delete', 'patch', 'options', 'head']

app = Flask(__name__, static_folder=STATIC_DIR)

def list_routes(startpath):
    routes = []

    for root, _, files in os.walk(startpath):
        if 'index.py' in files:
            uri = root
            if not uri.endswith('/'):
                uri += '/'

            routes.append(uri)

    return routes

def route_to_uri(route):
    return route.replace(ROUTES_DIR, '')

def route_to_name(route):
    return re.sub(r'>?/<?', '_', route_to_uri(route))

def route_to_mod_name(route):
    return 'routes' + route_to_name(route).replace('_', '.') + 'index'

def route_to_index(route):
    return os.path.join(route, 'index.py')

def add_routes_to_app():
    for route in list_routes(ROUTES_DIR):
        spec = importlib.util.spec_from_file_location(route_to_mod_name(route), route_to_index(route))

        if spec is None or spec.loader is None:
            print('No spec found for {}'.format(route_to_index(route)))
            continue

        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        for method_name in METHOD_NAMES:
            method = getattr(mod, method_name, None)

            if method is None:
                continue

            app.add_url_rule(route_to_uri(route), route_to_name(route), method, methods=[method_name.upper()])

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
    dev()
