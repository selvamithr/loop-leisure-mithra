"""
Loop & Leisure by Mithra - Customer Models
SQLAlchemy database mappings for customer accounts and their delivery addresses.
"""

from datetime import datetime
from app.database import db


class Customer(db.Model):
    """Represents a registered customer on the storefront."""
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_verified = db.Column(db.Boolean, default=False)

    # ── Relationships ──
    addresses = db.relationship('Address', back_populates='customer',
                                cascade='all, delete-orphan')
    cart = db.relationship('Cart', back_populates='customer',
                           uselist=False, cascade='all, delete-orphan')
    orders = db.relationship('Order', back_populates='customer')
    reviews = db.relationship('Review', back_populates='customer',
                              cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Customer {self.id}: {self.full_name}>'


class Address(db.Model):
    """Represents a delivery address linked to a customer account."""
    __tablename__ = 'addresses'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address_line1 = db.Column(db.String(255), nullable=False)
    address_line2 = db.Column(db.String(255), default='')
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    country = db.Column(db.String(100), default='India')
    is_default = db.Column(db.Boolean, default=False)

    # ── Relationships ──
    customer = db.relationship('Customer', back_populates='addresses')

    def __repr__(self):
        return f'<Address {self.id}: {self.city}, {self.state}>'
