"""
This is the main entry point for Coder Directory Api

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details.
"""

import flask
import coder_directory_api.settings as settings
import coder_directory_api.resources as resources
from coder_directory_api.auth import google_bp
from werkzeug.contrib.fixers import ProxyFix


def create_app() -> flask.Flask:
    """Factory method to create an instance of Coder Directory Api

    Returns:
        Instance of coder directory api
    """

    api = flask.Flask('__name__')
    api.wsgi_app = ProxyFix(api.wsgi_app)
    api.url_map.strict_slashes = False
    api.secret_key = settings.SECRET_KEY
    api.register_blueprint(
        resources.languages_api,
        url_prefix='{}/languages'.format(settings.BASE_URL)
    )
    api.register_blueprint(
        resources.users_api,
        url_prefix='{}/users'.format(settings.BASE_URL)
    )
    api.register_blueprint(
        resources.home_api,
        url_prefix=settings.BASE_URL
    )
    api.register_blueprint(google_bp)

    return api


if __name__ == '__main__':
    app = create_app()
    app.run(host=settings.HOST,
            port=settings.PORT,
            debug=settings.DEBUG,
            threaded=settings.MULTITHREADING)
