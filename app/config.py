import os
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

class Config:
    # Use the environment variable SECRET_KEY if available; otherwise, use a default value
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_default_secret_key')
    
    # Session settings
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    
    # Debug mode configuration
    DEBUG = os.environ.get('FLASK_DEBUG', '0') == '1'
    
    # SQLAlchemy settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    _db_url = os.environ.get('DATABASE_URL', 'postgresql://gitoptima_user:17mmyusuuf@localhost/gitoptima')
    if _db_url.startswith("postgres://"):
        _db_url = _db_url.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URI = _db_url
    
    # OAuth configurations
    GITHUB_CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID')
    GITHUB_CLIENT_SECRET = os.environ.get('GITHUB_CLIENT_SECRET')
    
    # Ensure these are set for OAuth to work
    if not GITHUB_CLIENT_ID or not GITHUB_CLIENT_SECRET:
        raise ValueError("GitHub OAuth settings not configured properly")

    # Ensure SECRET_KEY is set
    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for Flask application")

# Further config
