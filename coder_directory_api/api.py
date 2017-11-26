"""
This is the main entry point for Coder Directory Api

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details.
"""

import flask
import coder_directory_api.settings as settings
from coder_directory_api.resources import blueprint
from coder_directory_api.auth import google_bp
from flask_dance.contrib.google import google

def create_app() -> flask.Flask:
    """Factory method to create an instance of Coder Directory Api

    Returns:
        Instance of coder directory api
    """

    api = flask.Flask('__name__')
    api.url_map.strict_slashes = False
    api.secret_key = settings.SECRET_KEY
    api.register_blueprint(blueprint)
    api.register_blueprint(google_bp)

    return api


if __name__ == '__main__':
    app = create_app()

    @app.route('/test')
    def test():
        if not google.authorized:
            return flask.redirect(flask.url_for('google.login'))
        res = google.get('/oauth2/v2/userinfo')
        print(res.json())
        return 'Your email is {}'.format(res.json()['email'])


    app.run(host=settings.HOST,
            port=settings.PORT,
            debug=settings.DEBUG,
            threaded=settings.MULTITHREADING)
