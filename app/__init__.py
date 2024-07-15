from flask import Flask
from .routes import main as main_blueprint
from flask_oauthlib.client import OAuth
from flask_migrate import Migrate
from .config import Config
from .extensions import db
import os

# Ensure db is used appropriately within the application factory if necessary
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

    # Load configuration from config.py
    app.config.from_object(Config)

    # Configure session to use filesystem
    app.config['SESSION_TYPE'] = 'filesystem'

    # Initialize the database
    db.init_app(app)

    # Initialize Flask-Migrate
    migrate = Migrate(app, db)

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
