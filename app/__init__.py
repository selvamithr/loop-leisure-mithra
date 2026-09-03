"""
Loop & Leisure by Mithra - Application Factory
Creates and configures the Flask application instance using the Application Factory Pattern.
Initializes database connections, configures global folders, and registers Blueprints.
"""

import os
from flask import Flask
from app.config import config_by_name
from app.database import db

def create_app(config_name='development'):
    """
    Initializes and configures the Flask Application.
    Args:
        config_name (str): Configuration environment key ('development', 'production', 'testing')
    Returns:
        app (Flask): Configured Flask application instance
    """
    app = Flask(__name__, instance_relative_config=True)
    
    # Apply configuration parameters
    app.config.from_object(config_by_name[config_name])
    
    # Ensure required runtime directories exist (e.g., database instance and static upload folders)
    ensure_directories_exist(app)
    
    # Bind database settings
    db.init_app(app)
    
    # Register modular blueprints
    register_blueprints(app)
    
    return app

def ensure_directories_exist(app):
    """
    Ensures structural folders (instance and uploads) exist on the server.
    """
    # Ensure instance directory (root level) exists
    os.makedirs(app.instance_path, exist_ok=True)
    
    # Ensure file upload target folders exist
    os.makedirs(app.config['UPLOAD_FOLDER_PRODUCTS'], exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER_PAYMENTS'], exist_ok=True)

def register_blueprints(app):
    """
    Registers blueprints to map sub-routes.
    """
    from app.customer import customer_bp
    from app.admin import admin_bp
    
    # Customer-facing storefront blueprint (runs at base url prefix '/')
    app.register_blueprint(customer_bp, url_prefix='/')
    
    # Admin administration dashboard blueprint (runs at URL prefix '/admin')
    app.register_blueprint(admin_bp, url_prefix='/admin')
