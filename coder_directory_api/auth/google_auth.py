"""
Google OAuth for Coder Directory Api

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details.
"""

from flask_dance.contrib.google import make_google_blueprint

google_bp = make_google_blueprint(
    client_id='551381493649-bh5ll1k1433ob4t2u0bsearqt4ul81q0.apps.googleusercontent.com',
    client_secret='uJJejrWskjy1U8OU0zRcdiNR',
    scope=['profile', 'email']
)