"""
Loop & Leisure by Mithra - Application Configuration
Contains class configurations for Development, Production, and Testing stages.
Stores core settings, database URIs, security keys, and path definitions.
"""

import os

# Base directory of the application
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class Config:
    """Base configurations inherited by specific environments."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev_key_loop_leisure_mithra_secret_9982')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Maximum allowable file upload size (16MB)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    
    # Upload folder destinations relative to workspace
    UPLOAD_FOLDER_PRODUCTS = os.path.join(BASE_DIR, 'app', 'static', 'uploads', 'products')
    UPLOAD_FOLDER_PAYMENTS = os.path.join(BASE_DIR, 'app', 'static', 'uploads', 'payments')

class DevelopmentConfig(Config):
    """Development environment specific configuration."""
    DEBUG = True
    # Database stored in local instance directory
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'database.db')}"

class ProductionConfig(Config):
    """Production environment specific configuration."""
    DEBUG = False
    TESTING = False
    # Expects secure environment variable settings for production database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

class TestingConfig(Config):
    """Testing environment specific configuration."""
    TESTING = True
    # Use in-memory SQLite database for test speed and isolation
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

# Dictionary to map environment name to its respective class config
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
