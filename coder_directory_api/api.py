"""
This is the main entry point for Coder Directory Api

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details.
"""

import flask
import coder_directory_api.settings as settings
from coder_directory_api.resources import api
from werkzeug.contrib.fixers import ProxyFix


# Bootstrap api and engines
app = flask.Flask('__name__')
api.init_app(app)


if __name__ == '__main__':
    app.run(host=settings.HOST,
            port=settings.PORT,
            debug=settings.DEBUG,
            threaded=settings.MULTITHREADING)
