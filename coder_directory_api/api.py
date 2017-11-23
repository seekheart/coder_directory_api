"""
This is the main entry point for Coder Directory Api

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details.
"""

import flask
import coder_directory_api.settings as settings
from coder_directory_api.resources import blueprint
from werkzeug.contrib.fixers import ProxyFix


app = flask.Flask('__name__')
app.wsgi_app = ProxyFix(app.wsgi_app)
app.register_blueprint(blueprint)



if __name__ == '__main__':
    app.run(host=settings.HOST,
            port=settings.PORT,
            debug=settings.DEBUG,
            threaded=settings.MULTITHREADING)
