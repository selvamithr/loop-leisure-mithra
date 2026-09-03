"""
Loop & Leisure by Mithra - Admin Blueprint
Initializes and configurations routing rules for the administrative dashboard workspace.
"""

from flask import Blueprint

# Initialize the admin panel blueprint
admin_bp = Blueprint('admin', __name__)

# Import routes to register endpoints on the blueprint
from app.admin import routes
