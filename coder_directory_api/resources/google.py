"""
Google resource for Coder Directory

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details.
"""

from flask import Blueprint, jsonify, redirect, request
from coder_directory_api.settings import GOOGLE_SECRETS
from coder_directory_api.engines.auth_engine import AuthEngine
import coder_directory_api.auth as auth

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
flow.redirect_uri = 'http://localhost:3000/api/google/callback'
authorization_url, state = flow.authorization_url(
    access_type='offline',
    include_granted_scopes='true'
)

# setup white list for valid issuers
white_list = ['accounts.google.com', 'https://accounts.google.com']


@api.route('/', methods=['GET', 'POST'])
def google_login() -> redirect:
    """
    Google OAuth login resource for initiating OAuth Protocol.
    Returns:
        redirect to google login page.
    """
    if request.method == 'GET':
        return redirect(authorization_url)
    elif request.method == 'POST':
        data = request.get_json()
        token = data['token']
        client_id = data['clientId']

        is_valid, data = _validate_google_token(
            token=token,
            client_id=client_id
        )

        if is_valid:
            user = auth_engine.find_one(data)
            if not user:
                return jsonify({'message': 'User not registered!'}), 404
            return jsonify(user)
        else:
            return jsonify({'message': data})


@api.route('/callback')
def callback_url() -> None:
    """
    Callback uri for handling the second piece of google OAuth after user has
    consented.
    Returns:
        Nothing.
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


def _validate_google_token(token, client_id) -> tuple:
    """
    Helper function to validate a google oauth token

    Args:
        token: google token
        client_id: application id which was used to get token.

    Returns:
        indicator as to whether google token is valid or not and
        message/username.
    """

    try:
        id_info = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            client_id)
        if id_info['iss'] not in white_list:
            raise ValueError('Wrong Issuer!')
        user_name = id_info['email']
    except ValueError:
        return False, 'Invalid Google token!'

    return True, user_name