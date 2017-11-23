"""
This is the main entry point for Coder Directory Api

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details.
"""

import flask
import coder_directory_api.settings as settings
from coder_directory_api.resources import blueprint


def create_app() -> flask.Flask:
    """Factory method to create an instance of Coder Directory Api

    Returns:
        Instance of coder directory api
    """

    api = flask.Flask('__name__')
    api.url_map.strict_slashes = False
    api.register_blueprint(blueprint)
    return api


if __name__ == '__main__':
    app = create_app()
    app.run(host=settings.HOST,
            port=settings.PORT,
            debug=settings.DEBUG,
            threaded=settings.MULTITHREADING)
