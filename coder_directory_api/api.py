"""Api
This is the main entry point.

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details.
"""

import flask
import coder_directory_api.settings as settings


api = flask.Flask('__name__')


@api.route('/')
def home():
    return 'success!'




if __name__ == '__main__':
    api.run(host=settings.HOST,
            port=settings.PORT,
            debug=settings.DEBUG,
            threaded=settings.MULTITHREADING)