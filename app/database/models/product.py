"""
Loop & Leisure by Mithra - Product Models
SQLAlchemy database mappings for product catalog, product images, and customer reviews.
"""

from datetime import datetime
from app.database import db


class Product(db.Model):
    """Represents a crochet product in the store catalog."""
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    category = db.Column(db.String(100), nullable=False, index=True)
    price = db.Column(db.Float, nullable=False)
    advance_percentage = db.Column(db.Integer, default=50)
    stock_status = db.Column(db.String(20), default='available')
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ── Relationships ──
    images = db.relationship('ProductImage', back_populates='product',
                             cascade='all, delete-orphan')
    reviews = db.relationship('Review', back_populates='product',
                              cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Product {self.id}: {self.name}>'


class ProductImage(db.Model):
    """Represents an image associated with a product."""
    __tablename__ = 'product_images'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    image_path = db.Column(db.String(500), nullable=False)
    display_order = db.Column(db.Integer, default=0)

    # ── Relationships ──
    product = db.relationship('Product', back_populates='images')

    def __repr__(self):
        return f'<ProductImage {self.id}: Product {self.product_id}>'


class Review(db.Model):
    """Represents a customer review for a product. Only approved reviews are publicly visible."""
    __tablename__ = 'reviews'
    __table_args__ = (
        db.UniqueConstraint('customer_id', 'product_id', name='uq_customer_product_review'),
    )

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved = db.Column(db.Boolean, default=False)

    # ── Relationships ──
    customer = db.relationship('Customer', back_populates='reviews')
    product = db.relationship('Product', back_populates='reviews')

    def __repr__(self):
        return f'<Review {self.id}: Product {self.product_id} by Customer {self.customer_id}>'
