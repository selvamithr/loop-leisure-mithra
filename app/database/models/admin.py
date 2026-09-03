"""
Loop & Leisure by Mithra - Admin Model
SQLAlchemy database mappings for administrative operators and access roles.
"""

from app.database import db


class AdminUser(db.Model):
    """Represents an admin user with dashboard access."""
    __tablename__ = 'admin_users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(50), default='admin')

    def __repr__(self):
        return f'<AdminUser {self.id}: {self.name} ({self.role})>'
