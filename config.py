import os
from dotenv import load_dotenv

# Load .env if present
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'krishimitra-secret-key-2026-agro-secure')
    
    # MySQL Database Configurations
    MYSQL_HOST = os.environ.get('MYSQL_HOST', '127.0.0.1')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', '3306'))
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'krishimitra')
    MYSQL_UNIX_SOCKET = os.environ.get('MYSQL_UNIX_SOCKET', '')
    
    # SQLite fallback database file if MySQL server is not running
    SQLITE_DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'krishimitra.db')
    
    # Session Configuration
    SESSION_COOKIE_NAME = 'krishimitra_session'
    PERMANENT_SESSION_LIFETIME = 86400  # 1 day in seconds
    
    # Application settings
    APP_NAME = 'KrishiMitra'
    TAGLINE = 'Smart Farmer Assistance Platform'
