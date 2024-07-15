from flask import (
    Flask, session, flash, render_template, request, redirect,
    url_for, current_app, jsonify, make_response, Blueprint
)
from flask_oauthlib.client import OAuth
from flask_wtf import FlaskForm
from wtforms import Form, StringField
from wtforms.validators import DataRequired, Email
from app.models import User
from .extensions import db
import os

# Removed the problematic import
from .models import User

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
@main.route('/home')
def home():
    return render_template('index.html')

@main.route('/features')
def features():
    return render_template('features.html')


@main.route('/get-started')
def get_started():
    return render_template('get_started.html')
@main.route('/login')
def login():
    return github.authorize(callback=url_for('.authorized', _external=True))


@main.route('/logout')
def logout():
    session.pop('github_token', None)
    session.pop('user', None)
    return redirect(url_for('.index'))


@main.route('/profile/view', endpoint='view_profile')
def profile():
    return render_template('profile.html')


@main.route('/login/authorized')
def authorized():

    response = github.authorized_response()
    if response is None or response.get('access_token') is None:
        error_reason = request.args.get('error', 'Unknown error')
        error_description = request.args.get(
           'error_description', 'No description provided'
            )
    return (
        f'Access denied: reason={error_reason} '
        f'error={error_description}'
    )

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


@main.route('/profile')
def profile():
    # Check if user is logged in
    if 'user' not in session:
        flash('Please log in to view your profile.', 'info')
        return redirect(url_for('.login'))

    # Fetch detailed user profile data from the database
    try:
        user_id = session['user']['id']
        user = User.query.get(user_id)
        if not user:
            flash('User not found.', 'error')
            return redirect(url_for('.login'))
    except Exception as e:
        flash('An error occurred while fetching user data.', 'error')
        current_app.logger.error(f'Error fetching user data: {e}')
        return redirect(url_for('.login'))

    return render_template('profile.html', user=user)


class EditProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])


@main.route('/profile/edit', methods=['GET', 'POST'])
def edit_profile():
    if 'user' not in session:
        return redirect(url_for('.login'))

    user_id = session['user']['id']
    user = User.query.get(user_id)
    form = EditProfileForm(obj=user)

    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data
        db.session.commit()
        session['user']['name'] = user.name
        session['user']['email'] = user.email
        flash('Profile updated successfully!')
        return redirect(url_for('.profile'))

    return render_template('edit_profile.html', form=form)
