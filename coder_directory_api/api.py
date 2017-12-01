"""
This is the main entry point for Coder Directory Api

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details.
"""

import flask
import coder_directory_api.settings as settings
import coder_directory_api.resources as resources
from flask_cors import CORS
from werkzeug.contrib.fixers import ProxyFix


def create_app() -> flask.Flask:
    """Factory method to create an instance of Coder Directory Api

    Returns:
        Instance of coder directory api
    """

    api = flask.Flask('__name__')
    CORS(api)
    api.wsgi_app = ProxyFix(api.wsgi_app)
    api.url_map.strict_slashes = False

    for rsc in resources.api_resources:

        register_resources(
            api,
            bp=rsc['bp'],
            route=rsc['route']
        )

    return api


def register_resources(api, bp, route=None):
    if route:
        return api.register_blueprint(
            bp,
            url_prefix='{}/{}'.format(settings.BASE_URL, route)
        )
    return api.register_blueprint(
        bp,
        url_prefix=settings.BASE_URL
    )

if __name__ == '__main__':
    app = create_app()
    app.run(host=settings.HOST,
            port=settings.PORT,
            debug=settings.DEBUG,
            threaded=settings.MULTITHREADING)
