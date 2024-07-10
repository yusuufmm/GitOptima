from flask import Blueprint, render_template, redirect, url_for, session
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
    session.pop('github_token')
    return redirect(url_for('.index'))

@main.route('/login/authorized')
def authorized():
    response = github.authorized_response()
    if response is None or response.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error'], request.args['error_description']
        )
    session['github_token'] = (response['access_token'], '')
    user_info = github.get('user')
    return 'Logged in as: ' + user_info.data['login']

@github.tokengetter
def get_github_oauth_token():
    return session.get('github_token')

