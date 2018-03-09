"""
Google resource for Coder Directory

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details.
"""

from flask import Blueprint, jsonify, redirect, request
from coder_directory_api.settings import GOOGLE_SECRETS, PORT, google_secrets
from coder_directory_api.engines.auth_engine import AuthEngine
import coder_directory_api.auth as auth
from coder_directory_api.auth import refresh_token

import google_auth_oauthlib.flow
import googleapiclient.discovery
from google.oauth2 import id_token
from google.auth.transport import requests

api = Blueprint('google', __name__)
auth_engine = AuthEngine()

# setup a flow object to manage OAuth exchange.
flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    GOOGLE_SECRETS,
    scopes=[
        'https://www.googleapis.com/auth/plus.login',
        'https://www.googleapis.com/auth/plus.me',
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile',
    ])
flow.redirect_uri = 'http://localhost:{}/api/google/callback'.format(PORT)
authorization_url, state = flow.authorization_url(
    access_type='offline',
    include_granted_scopes='true'
)

# setup white list for valid issuers
white_list = ['accounts.google.com', 'https://accounts.google.com']


@api.route('/', methods=['GET'])
def google_login() -> redirect or tuple:
    """
    Google OAuth login resource for initiating OAuth Protocol.
    Returns:
        redirect to google login page if no auth token provided, otherwise,
        api will return api access and refresh tokens if google token is valid
        along with 200 status code, or 400 status code with error message if
        google token.
    """
    if request.method == 'GET':
        try:
            auth_token = request.headers['Authorization'].split(' ')[1]
            is_valid, data = _validate_google_token(auth_token)
        except KeyError:
            return redirect(authorization_url)

        if is_valid:
            user = auth_engine.find_one(data)
            if not user:
                return jsonify({'message': 'User not registered!'}), 404
            user_tokens = {
                'user': user['user'],
                'access_token': user['access_token'],
                'refresh_token': user['refresh_token']
            }
            new_tokens = refresh_token(user_tokens)
            return jsonify(new_tokens)
        else:
            return jsonify({'message': data}), 400


@api.route('/callback')
def callback_url() -> None:
    """
    Callback uri for handling the second piece of google OAuth after user has
    consented.
    Returns:
        api access and refresh tokens
    """
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials
    d = googleapiclient.discovery.build('oauth2', 'v2', credentials=credentials)
    data = d.userinfo().v2().me().get().execute()
    auth_doc = {'user': data['email'], 'googleId': data['id']}
    auth_engine.add_one(auth_doc)
    payload = auth.make_token(auth_doc['user'])
    return jsonify(payload)


def _validate_google_token(token) -> tuple:
    """
    Helper function to validate a google oauth token

    Args:
        token: google token

    Returns:
        indicator as to whether google token is valid or not and
        message/username.
    """

    try:
        id_info = id_token.verify_oauth2_token(token, requests.Request())
        if id_info['iss'] not in white_list:
            raise ValueError('Wrong Issuer!')
        user_name = id_info['email']
    except ValueError:
        return False, 'Invalid Google token!'
    return True, user_name
