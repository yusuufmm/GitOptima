from flask import Blueprint, redirect, url_for, session, request, jsonify
from flask_oauthlib.client import OAuth
import os

main = Blueprint('main', __name__)
oauth = OAuth()

# GitHub OAuth setup
github = oauth.remote_app(
    'github',
    consumer_key=os.environ.get('GITHUB_CLIENT_ID'),
    consumer_secret=os.environ.get('GITHUB_CLIENT_SECRET'),
    request_token_params={'scope': 'user:email'},
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize'
)

@main.route('/')
def index():
    return 'Welcome to GitOptima!'

@main.route('/login')
def login():
    return github.authorize(callback=url_for('.authorized', _external=True))

@main.route('/logout')
def logout():
    session.pop('github_token', None)
    session.pop('user', None)
    return redirect(url_for('.index'))

@main.route('/login/authorized')
def authorized():
    response = github.authorized_response()
    if response is None or response.get('access_token') is None:
        error_reason = request.args.get('error', 'Unknown error')
        error_description = request.args.get('error_description', 'No description provided')
        return f'Access denied: reason={error_reason} error={error_description}'

    session['github_token'] = (response['access_token'], '')
    user_info = github.get('user')

    if user_info.data:
        session['user'] = user_info.data
        return redirect(url_for('.index'))
    else:
        return 'Failed to fetch user info from GitHub.'

@github.tokengetter
def get_github_oauth_token():
    return session.get('github_token')

# Additional routes can be added here

