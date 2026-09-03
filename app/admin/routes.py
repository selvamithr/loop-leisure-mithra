"""
Loop & Leisure by Mithra - Admin Dashboard Routes
Contains controller logic, dashboard cards, payment verification/rejection, production status updates, shipping details, and route protection.
"""

from functools import wraps
from flask import render_template, session, request, redirect, url_for, flash, current_app
from werkzeug.security import check_password_hash
from app.admin import admin_bp
from app.database import db
from app.database.models import AdminUser, Customer, Order, OrderItem, Payment, Product, ContactMessage
from datetime import datetime

# ── Admin Authentication Decorator ──
def admin_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Please log in as an administrator to access this area.', 'error')
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

# ── Admin Auth Routes ──
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'admin_id' in session:
        return redirect(url_for('admin.dashboard'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Email and password are required.', 'error')
            return redirect(url_for('admin.login'))
            
        admin = AdminUser.query.filter_by(email=email).first()
        if not admin or not check_password_hash(admin.password_hash, password):
            flash('Invalid admin credentials.', 'error')
            return redirect(url_for('admin.login'))
            
        session['admin_id'] = admin.id
        flash(f'Logged in successfully as {admin.name}!', 'success')
        return redirect(url_for('admin.dashboard'))
        
    return render_template('admin/login.html')

@admin_bp.route('/logout')
def logout():
    session.pop('admin_id', None)
    flash('Logged out from admin panel.', 'success')
    return redirect(url_for('admin.login'))

# ── Admin Dashboard ──
@admin_bp.route('/')
@admin_bp.route('/dashboard')
@admin_login_required
def dashboard():
    total_orders = Order.query.count()
    pending_payments = Payment.query.filter_by(status='Pending').count()
    orders_in_production = Order.query.filter_by(production_status='Started').count()
    completed_orders = Order.query.filter_by(production_status='Completed').count()
    
    # Ready for Dispatch: Production Completed AND Payment Fully Paid AND Order Confirmed (not dispatched yet)
    ready_for_dispatch = Order.query.filter_by(
        production_status='Completed',
        payment_status='Fully Paid',
        order_status='Confirmed'
    ).count()
    
    delivered_orders = Order.query.filter_by(order_status='Delivered').count()
    total_customers = Customer.query.count()
    
    # Let's fetch recent orders for dashboard summary
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                           total_orders=total_orders,
                           pending_payments=pending_payments,
                           orders_in_production=orders_in_production,
                           completed_orders=completed_orders,
                           ready_for_dispatch=ready_for_dispatch,
                           delivered_orders=delivered_orders,
                           total_customers=total_customers,
                           recent_orders=recent_orders)

# ── Admin Orders List ──
@admin_bp.route('/orders')
@admin_login_required
def orders():
    all_orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin/orders.html', orders=all_orders)

# ── Admin Order Details ──
@admin_bp.route('/order/<order_number>')
@admin_login_required
def order_details(order_number):
    order = Order.query.filter_by(order_number=order_number).first_or_404()
    return render_template('admin/order_details.html', order=order)

# ── Admin Payment Verification Actions ──
@admin_bp.route('/order/<order_number>/payment/<int:payment_id>/verify', methods=['POST'])
@admin_login_required
def verify_payment(order_number, payment_id):
    order = Order.query.filter_by(order_number=order_number).first_or_404()
    payment = Payment.query.get_or_404(payment_id)
    
    if payment.order_id != order.id:
        flash('Payment does not belong to this order.', 'error')
        return redirect(url_for('admin.order_details', order_number=order.order_number))
        
    payment.verified_by_admin = True
    payment.status = 'Verified'
    payment.verified_at = datetime.utcnow()
    
    # Automatically update statuses:
    if payment.payment_type == 'Advance':
        order.payment_status = 'Advance Paid'
        order.order_status = 'Confirmed'
        order.production_status = 'Started'
    elif payment.payment_type == 'Final':
        order.payment_status = 'Fully Paid'
        # Production remains Completed, order remains Confirmed until Dispatched
        
    db.session.commit()
    flash(f'{payment.payment_type} Payment verified successfully. Order statuses updated.', 'success')
    return redirect(url_for('admin.order_details', order_number=order.order_number))

@admin_bp.route('/order/<order_number>/payment/<int:payment_id>/reject', methods=['POST'])
@admin_login_required
def reject_payment(order_number, payment_id):
    order = Order.query.filter_by(order_number=order_number).first_or_404()
    payment = Payment.query.get_or_404(payment_id)
    rejection_reason = request.form.get('rejection_reason')
    
    if not rejection_reason:
        flash('Rejection reason is required.', 'error')
        return redirect(url_for('admin.order_details', order_number=order.order_number))
        
    if payment.order_id != order.id:
        flash('Payment does not belong to this order.', 'error')
        return redirect(url_for('admin.order_details', order_number=order.order_number))
        
    payment.verified_by_admin = False
    payment.status = 'Rejected'
    payment.rejection_reason = rejection_reason
    
    # Set payment status back to Rejected, so customer can re-upload screenshot
    order.payment_status = 'Rejected'
    
    db.session.commit()
    flash('Payment rejected. Customer will be prompted to re-upload proof.', 'info')
    return redirect(url_for('admin.order_details', order_number=order.order_number))

# ── Admin Production Updates ──
@admin_bp.route('/order/<order_number>/production', methods=['POST'])
@admin_login_required
def update_production(order_number):
    order = Order.query.filter_by(order_number=order_number).first_or_404()
    status = request.form.get('production_status')
    
    if status not in ('Not Started', 'Started', 'Completed'):
        flash('Invalid production status.', 'error')
        return redirect(url_for('admin.order_details', order_number=order.order_number))
        
    if status in ('Started', 'Completed') and order.payment_status not in ('Advance Paid', 'Fully Paid'):
        flash('Cannot start production: Payment has not been approved yet.', 'error')
        return redirect(url_for('admin.order_details', order_number=order.order_number))
        
    order.production_status = status
    db.session.commit()
    flash(f'Production status updated to {status}.', 'success')
    return redirect(url_for('admin.order_details', order_number=order.order_number))

# ── Admin Request Remaining Payment ──
@admin_bp.route('/order/<order_number>/request-remaining', methods=['POST'])
@admin_login_required
def request_remaining(order_number):
    order = Order.query.filter_by(order_number=order_number).first_or_404()
    
    if order.production_status != 'Completed':
        flash('Cannot request final payment until production is Completed.', 'error')
        return redirect(url_for('admin.order_details', order_number=order.order_number))
        
    order.payment_status = 'Remaining Pending'
    db.session.commit()
    flash('Remaining payment requested. Customer can now submit the final payment.', 'success')
    return redirect(url_for('admin.order_details', order_number=order.order_number))

# ── Admin Dispatch Action ──
@admin_bp.route('/order/<order_number>/dispatch', methods=['POST'])
@admin_login_required
def dispatch_order(order_number):
    order = Order.query.filter_by(order_number=order_number).first_or_404()
    courier_name = request.form.get('courier_name')
    tracking_number = request.form.get('tracking_number')
    
    if not courier_name or not tracking_number:
        flash('Courier name and tracking number are required.', 'error')
        return redirect(url_for('admin.order_details', order_number=order.order_number))
        
    order.courier_name = courier_name
    order.tracking_number = tracking_number
    order.dispatch_date = datetime.utcnow()
    order.order_status = 'Dispatched'
    
    db.session.commit()
    flash('Order marked as Dispatched. Courier details recorded.', 'success')
    return redirect(url_for('admin.order_details', order_number=order.order_number))

# ── Admin Delivery Action ──
@admin_bp.route('/order/<order_number>/delivery', methods=['POST'])
@admin_login_required
def deliver_order(order_number):
    order = Order.query.filter_by(order_number=order_number).first_or_404()
    order.order_status = 'Delivered'
    db.session.commit()
    flash('Order marked as Delivered.', 'success')
    return redirect(url_for('admin.order_details', order_number=order.order_number))


# ── Admin Products ──
@admin_bp.route('/products')
@admin_login_required
def admin_products():
    from app.database.models import Product
    products = Product.query.filter(Product.stock_status != 'archived').order_by(Product.created_at.desc()).all()
    return render_template('admin/products.html', products=products)

@admin_bp.route('/products/add', methods=['GET', 'POST'])
@admin_login_required
def product_add():
    from app.database.models import Product
    if request.method == 'POST':
        name = request.form.get('name')
        slug = request.form.get('slug') or name.lower().replace(' ', '-')
        description = request.form.get('description')
        category = request.form.get('category')
        price = request.form.get('price')
        stock_status = request.form.get('stock_status')
        
        # Check if slug exists
        if Product.query.filter_by(slug=slug).first():
            slug = slug + '-' + str(int(datetime.utcnow().timestamp()))
            
        new_prod = Product(
            name=name,
            slug=slug,
            description=description,
            category=category,
            price=float(price) if price else 0.0,
            stock_status=stock_status
        )
        db.session.add(new_prod)
        db.session.commit()
        flash('Product added successfully.', 'success')
        return redirect(url_for('admin.admin_products'))
    return render_template('admin/product_form.html', product=None)

@admin_bp.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
@admin_login_required
def product_edit(product_id):
    from app.database.models import Product
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.slug = request.form.get('slug')
        product.description = request.form.get('description')
        product.category = request.form.get('category')
        product.price = float(request.form.get('price')) if request.form.get('price') else 0.0
        product.stock_status = request.form.get('stock_status')
        
        db.session.commit()
        flash('Product updated successfully.', 'success')
        return redirect(url_for('admin.admin_products'))
    return render_template('admin/product_form.html', product=product)

@admin_bp.route('/products/delete/<int:product_id>', methods=['POST'])
@admin_login_required
def product_delete(product_id):
    from app.database.models import Product
    product = Product.query.get_or_404(product_id)
    # Soft delete to preserve historical orders
    product.stock_status = 'archived'
    db.session.commit()
    flash('Product deleted (archived).', 'success')
    return redirect(url_for('admin.admin_products'))

# ── Admin Contact Messages ──
@admin_bp.route('/contact-messages')
@admin_login_required
def contact_messages():
    """Display all contact enquiries for admin."""
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template('admin/contact_messages.html', messages=messages)

@admin_bp.route('/contact-messages/<int:msg_id>/delete', methods=['POST'])
@admin_login_required
def delete_contact_message(msg_id):
    msg = ContactMessage.query.get_or_404(msg_id)
    db.session.delete(msg)
    db.session.commit()
    flash('Message deleted.', 'success')
    return redirect(url_for('admin.contact_messages'))

@admin_bp.route('/contact-messages/<int:msg_id>/mark-read', methods=['POST'])
@admin_login_required
def mark_contact_message_read(msg_id):
    msg = ContactMessage.query.get_or_404(msg_id)
    from app.database.models import MessageStatus
    msg.status = MessageStatus.READ
    db.session.commit()
    flash('Message marked as read.', 'success')
    return redirect(url_for('admin.contact_messages'))

@admin_bp.route('/contact-messages/<int:msg_id>/mark-replied', methods=['POST'])
@admin_login_required
def mark_contact_message_replied(msg_id):
    msg = ContactMessage.query.get_or_404(msg_id)
    from app.database.models import MessageStatus
    msg.status = MessageStatus.REPLIED
    db.session.commit()
    flash('Message marked as replied.', 'success')
    return redirect(url_for('admin.contact_messages'))
