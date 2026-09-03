"""
Loop & Leisure by Mithra - Database Module
Instantiates the SQLAlchemy ORM handler for model mapping and operations.
"""

from flask_sqlalchemy import SQLAlchemy

# Declare db context extension to be initialized in create_app()
db = SQLAlchemy()
