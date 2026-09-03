"""
Loop & Leisure by Mithra - Models Package
Consolidates and exposes SQLAlchemy schema declarations for the application database.
"""



from app.database.models.admin import AdminUser
from app.database.models.customer import Customer, Address
from app.database.models.product import Product, ProductImage, Review
from app.database.models.order import Cart, CartItem, Order, OrderItem, Payment
from app.database.models.contact_message import ContactMessage

# Expose models at the package level
__all__ = [
    'AdminUser',
    'Customer',
    'Address',
    'Product',
    'ProductImage',
    'Review',
    'Cart',
    'CartItem',
    'Order',
    'OrderItem',
    'Payment',
    'ContactMessage'
]
