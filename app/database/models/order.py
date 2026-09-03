"""
Loop & Leisure by Mithra - Order Models
SQLAlchemy database mappings for shopping cart, orders, order items, and payment records.
Implements the made-to-order crochet workflow with advance payment tracking.

Order Flow:
    Customer places order → Pays 50% advance → Admin verifies payment →
    Crocheting started → Completed → Customer pays remaining 50% →
    Dispatched → Delivered
"""

from datetime import datetime
from app.database import db


class Cart(db.Model):
    """Represents a customer's shopping cart (one cart per customer)."""
    __tablename__ = 'carts'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'),
                            nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ── Relationships ──
    customer = db.relationship('Customer', back_populates='cart')
    items = db.relationship('CartItem', back_populates='cart',
                            cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Cart {self.id}: Customer {self.customer_id}>'


class CartItem(db.Model):
    """Represents a single product entry within a customer's shopping cart."""
    __tablename__ = 'cart_items'
    __table_args__ = (
        db.UniqueConstraint('cart_id', 'product_id', name='uq_cart_product'),
    )

    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)

    # ── Relationships ──
    cart = db.relationship('Cart', back_populates='items')
    product = db.relationship('Product')

    def __repr__(self):
        return f'<CartItem {self.id}: Product {self.product_id} x{self.quantity}>'


class Order(db.Model):
    """
    Represents a placed customer order following the made-to-order workflow:
    Order Placed → Advance Paid → Payment Verified → Crocheting Started →
    Completed → Remaining Paid → Dispatched → Delivered
    """
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(20), unique=True, nullable=False, index=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'), nullable=False)

    # ── Financial fields ──
    subtotal = db.Column(db.Float, nullable=False)
    shipping_charge = db.Column(db.Float, default=0.0)
    advance_amount = db.Column(db.Float, nullable=False)
    remaining_amount = db.Column(db.Float, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)

    # ── Status tracking fields ──
    payment_status = db.Column(db.String(20), default='Pending', index=True)
    production_status = db.Column(db.String(20), default='Not Started', index=True)
    order_status = db.Column(db.String(20), default='Pending', index=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    courier_name = db.Column(db.String(100))
    tracking_number = db.Column(db.String(100))
    dispatch_date = db.Column(db.DateTime)

    # ── Relationships ──
    customer = db.relationship('Customer', back_populates='orders')
    address = db.relationship('Address')
    items = db.relationship('OrderItem', back_populates='order',
                            cascade='all, delete-orphan')
    payments = db.relationship('Payment', back_populates='order',
                               cascade='all, delete-orphan')

    # ── Valid status constants ──
    PAYMENT_STATUSES = ('Pending', 'Advance Paid', 'Fully Paid')
    PRODUCTION_STATUSES = ('Not Started', 'Started', 'Completed')
    ORDER_STATUSES = ('Pending', 'Confirmed', 'Dispatched', 'Delivered', 'Cancelled')

    @staticmethod
    def generate_order_number():
        """
        Generates a unique, beautiful order number in the format: LLM-YYYY-NNNNN
        Example: LLM-2026-00001, LLM-2026-00002, etc.
        LLM = Loop & Leisure Mithra
        """
        year = datetime.utcnow().year
        last_order = Order.query.filter(
            Order.order_number.like(f'LLM-{year}-%')
        ).order_by(Order.id.desc()).first()

        if last_order:
            last_seq = int(last_order.order_number.split('-')[-1])
            next_seq = last_seq + 1
        else:
            next_seq = 1

        return f'LLM-{year}-{next_seq:05d}'

    def __repr__(self):
        return f'<Order {self.order_number}: {self.order_status}>'


class OrderItem(db.Model):
    """Represents a single product line item within a placed order."""
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    # ── Relationships ──
    order = db.relationship('Order', back_populates='items')
    product = db.relationship('Product')

    def __repr__(self):
        return f'<OrderItem {self.id}: Product {self.product_id} x{self.quantity}>'


class Payment(db.Model):
    """
    Represents a payment record for an order.
    Each order can have up to two payments: Advance (50%) and Final (remaining 50%).
    Payment verification is manual via admin review of UPI reference and screenshot.
    """
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    payment_type = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    upi_reference = db.Column(db.String(100))
    payment_screenshot = db.Column(db.String(500))
    verified_by_admin = db.Column(db.Boolean, default=False)
    verified_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Pending') # 'Pending', 'Verified', 'Rejected'
    rejection_reason = db.Column(db.Text)

    # ── Relationships ──
    order = db.relationship('Order', back_populates='payments')

    # ── Valid payment types ──
    PAYMENT_TYPES = ('Advance', 'Final')

    def __repr__(self):
        return f'<Payment {self.id}: {self.payment_type} ₹{self.amount}>'
