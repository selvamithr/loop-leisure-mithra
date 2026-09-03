"""
Loop & Leisure by Mithra - Server Entrypoint
This script initializes and runs the Flask application.
It loads configuration settings and starts the WSGI server.
"""

import os
from dotenv import load_dotenv
from app import create_app

# Load environment variables from .env if present
load_dotenv()

# Determine configuration type from environment, fallback to 'development'
config_env = os.getenv('FLASK_CONFIG', 'development')
app = create_app(config_env)

if __name__ == '__main__':
    # Local development execution settings
    app.run(host='127.0.0.1', port=5000, debug=True)
