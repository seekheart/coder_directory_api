"""Api
This is the main entry point.

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details.
"""

import flask
import settings

app = flask.Flask('__name__')


@app.route('/')
def home():
    return 'success!'


if __name__ == '__main__':
    app.run(host=settings.HOST,
            port=settings.PORT,
            debug=settings.DEBUG,
            threaded=settings.MULTITHREADING)