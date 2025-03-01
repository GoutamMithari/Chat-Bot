import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration class."""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-for-cdp-support-chatbot')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    # Cache settings
    CACHE_ENABLED = True
    CACHE_TIMEOUT = 86400  # 24 hours in seconds

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    
class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    
class ProductionConfig(Config):
    """Production configuration."""
    # Production-specific settings
    pass

# Configure based on environment
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}

# Active configuration
active_config = config_by_name[os.getenv('FLASK_ENV', 'development')]