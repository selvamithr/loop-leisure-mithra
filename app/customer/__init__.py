"""
Loop & Leisure by Mithra - Customer Blueprint
Initializes routing rules and views for the client-facing store frontend.
"""

from flask import Blueprint

# Initialize the customer storefront blueprint
customer_bp = Blueprint('customer', __name__)

# Import routes to register endpoints on the blueprint
from app.customer import routes
