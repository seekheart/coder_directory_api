from flask import Blueprint, jsonify, redirect, request
from coder_directory_api.settings import GOOGLE_SECRETS
from coder_directory_api.engines.auth_engine import AuthEngine
import coder_directory_api.auth as auth

import google_auth_oauthlib.flow
import googleapiclient.discovery

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


@api.route('/', methods=['GET'])
def google_login() -> redirect:
    """
    Google OAuth login resource for initiating OAuth Protocol.
    Returns:
        redirect to google login page.
    """
    return redirect(authorization_url)


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
