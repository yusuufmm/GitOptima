from flask import Flask
import os
from flask_oauthlib.client import OAuth
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    """
    Create and configure the Flask application.
    Sets up GitHub OAuth for user authentication.

    Returns:
        app: The configured Flask application.
    """
    app = Flask(__name__)

    # Set the secret key for session management
    app.secret_key = os.environ.get('SECRET_KEY')

    # Load configuration from a separate config file
    app.config.from_pyfile('config.py')

    # Configure session to use filesystem (can also use 'redis', 'memcached', etc.)
    app.config['SESSION_TYPE'] = 'filesystem'

    # Initialize the database
    db.init_app(app)

    # Initialize OAuth
    oauth = OAuth(app)

    # Configure GitHub OAuth
    github = oauth.remote_app(
        'github',
        consumer_key=os.environ.get('GITHUB_CLIENT_ID'),
        consumer_secret=os.environ.get('GITHUB_CLIENT_SECRET'),
        request_token_params={
            'scope': 'user:email',
        },
        base_url='https://api.github.com/',
        request_token_url=None,
        access_token_method='POST',
        access_token_url='https://github.com/login/oauth/access_token',
        authorize_url='https://github.com/login/oauth/authorize'
    )

    # Import and register Blueprints
    from .routes import main
    app.register_blueprint(main)

    return app

