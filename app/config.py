import os
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for Flask application")
    
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    DEBUG = os.environ.get('FLASK_DEBUG', '0') == '1'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Correcting the DATABASE_URL for SQLAlchemy compatibility
    _db_url = os.environ.get('DATABASE_URL', 'sqlite:///site.db')
    if _db_url.startswith("postgres://"):
        _db_url = _db_url.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URI = _db_url

    # OAuth configurations
    GITHUB_CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID')
    GITHUB_CLIENT_SECRET = os.environ.get('GITHUB_CLIENT_SECRET')

    # Ensure these are set for OAuth to work
    if not GITHUB_CLIENT_ID or not GITHUB_CLIENT_SECRET:
        raise ValueError("GitHub OAuth settings not configured properly")

# Further config
