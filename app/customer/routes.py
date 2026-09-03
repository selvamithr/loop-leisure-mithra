"""
Loop & Leisure by Mithra - Customer Storefront Routes
Handles routing rules and controller functions for storefront pages and orders.
"""
from functools import wraps
from flask import render_template, session, request, jsonify, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.customer import customer_bp
from app.database import db
from app.database.models import Customer, Product, Cart, CartItem, Address, Order, OrderItem

# ── Authentication Decorator ──
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'customer_id' not in session:
            # Handle specific route messages
            if request.endpoint == 'customer.cart_add':
                flash('Please log in or create an account to add items to your cart.', 'error')
            elif request.endpoint == 'customer.checkout':
                flash('Please log in to continue with your order.', 'error')
            else:
                flash('Please log in to access this page.', 'error')
            
            # If AJAX request, return JSON redirect instruction (absolute URL)
            if request.is_json:
                return jsonify({
                    'success': False,
                    'redirect': url_for('customer.login', next=request.referrer or request.url, _external=True)
                }), 401
                
            # Non‑AJAX request – use relative URL (as expected by tests)
            return redirect(url_for('customer.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# ── Helper: get current customer ──
def _get_current_customer():
    """Returns the logged-in customer object."""
    customer_id = session.get('customer_id')
    if customer_id:
        return Customer.query.get(customer_id)
    return None

# ── Helper: get or create cart ──
def _get_cart():
    """Returns the Cart model instance for the logged-in user."""
    customer = _get_current_customer()
    if not customer:
        return None
        
    cart = Cart.query.filter_by(customer_id=customer.id).first()
    if not cart:
        cart = Cart(customer_id=customer.id)
        db.session.add(cart)
        db.session.commit()
    return cart

# ── Authentication Routes ──

@customer_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Customer registration route."""
    if 'customer_id' in session:
        return redirect(url_for('customer.index'))
        
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if not all([full_name, email, phone, password, confirm_password]):
            flash('All fields are required.', 'error')
            return redirect(url_for('customer.register'))
            
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('customer.register'))
            
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return redirect(url_for('customer.register'))
            
        # Check uniqueness
        if Customer.query.filter_by(email=email).first():
            flash('Email already exists. Please log in.', 'error')
            return redirect(url_for('customer.login'))
            
        if Customer.query.filter_by(phone=phone).first():
            flash('Phone number already registered.', 'error')
            return redirect(url_for('customer.register'))
            
        # Create user
        new_customer = Customer(
            full_name=full_name,
            email=email,
            phone=phone,
            password_hash=generate_password_hash(password)
        )
        db.session.add(new_customer)
        db.session.commit()
        
        # Log them in automatically
        session['customer_id'] = new_customer.id
        flash('Registration successful! Welcome to Loop & Leisure.', 'success')
        return redirect(url_for('customer.index'))
        
    return render_template('customer/register.html')

@customer_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Customer login route."""
    if 'customer_id' in session:
        return redirect(url_for('customer.index'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Email and password are required.', 'error')
            return redirect(url_for('customer.login'))
            
        customer = Customer.query.filter_by(email=email).first()
        
        if not customer or not check_password_hash(customer.password_hash, password):
            flash('Invalid email or password.', 'error')
            return redirect(url_for('customer.login'))
            
        session['customer_id'] = customer.id
        flash(f'Welcome back, {customer.full_name}!', 'success')
        
        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)
        return redirect(url_for('customer.index'))
        
    return render_template('customer/login.html')

@customer_bp.route('/logout')
def logout():
    """Customer logout route."""
    session.pop('customer_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('customer.index'))

# ── Page Routes ──

@customer_bp.route('/')
def index():
    return render_template('customer/index.html')

@customer_bp.route('/shop')
def shop():
    from app.database.models import Product
    products = Product.query.filter(Product.stock_status != 'archived').order_by(Product.created_at.desc()).all()
    return render_template('customer/shop.html', products=products)

@customer_bp.route('/product')
def product():
    from app.database.models import Product, Review, Order, OrderItem
    slug = request.args.get('slug', 'crochet-rose-bouquet')
    product = Product.query.filter_by(slug=slug).first_or_404()
    
    # Get approved reviews for this product
    db_reviews = Review.query.filter_by(product_id=product.id, approved=True).all()
    
    # Check if current customer is eligible to submit a review
    can_review = False
    customer = _get_current_customer()
    if customer:
        # User must not have reviewed this product already
        existing_review = Review.query.filter_by(customer_id=customer.id, product_id=product.id).first()
        if not existing_review:
            # User must have a delivered order containing this product
            delivered_order = Order.query.join(OrderItem).filter(
                Order.customer_id == customer.id,
                Order.order_status == 'Delivered',
                OrderItem.product_id == product.id
            ).first()
            if delivered_order:
                can_review = True
                
    return render_template('customer/product.html', 
                           product=product, 
                           db_reviews=db_reviews, 
                           can_review=can_review)

@customer_bp.route('/cart')
@login_required
def cart():
    cart = _get_cart()
    cart_items_data = []
    subtotal = 0.0

    if cart:
        for item in cart.items:
            product = item.product
            item_subtotal = round(product.price * item.quantity, 2)
            
            image_url = product.images[0].image_path if product.images else 'https://picsum.photos/seed/placeholder/500/600'
                
            cart_items_data.append({
                'id': product.slug, 
                'name': product.name,
                'category': product.category,
                'price': product.price,
                'quantity': item.quantity,
                'subtotal': item_subtotal,
                'image': image_url
            })
            subtotal += item_subtotal
    
    subtotal = round(subtotal, 2)
    shipping = 5.99 if cart_items_data else 0.00
    total = round(subtotal + shipping, 2)

    return render_template('customer/cart.html',
                           cart_items=cart_items_data,
                           subtotal=subtotal,
                           shipping=shipping,
                           total=total)

@customer_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    """Checkout route handling address selection and order creation."""
    customer = _get_current_customer()
    cart = _get_cart()
    
    if not cart or not cart.items:
        flash('Your cart is empty.', 'error')
        return redirect(url_for('customer.cart'))

    # Calculate totals
    subtotal = sum(round(item.product.price * item.quantity, 2) for item in cart.items)
    shipping_charge = 5.99 if subtotal > 0 else 0.0
    total_amount = round(subtotal + shipping_charge, 2)
    advance_amount = round(total_amount * 0.5, 2)
    remaining_amount = round(total_amount - advance_amount, 2)

    if request.method == 'POST':
        address_id = request.form.get('address_id')
        
        if address_id == 'new':
            # Create new address
            new_address = Address(
                customer_id=customer.id,
                name=request.form.get('name'),
                phone=request.form.get('phone'),
                address_line1=request.form.get('address_line1'),
                address_line2=request.form.get('address_line2', ''),
                city=request.form.get('city'),
                state=request.form.get('state'),
                pincode=request.form.get('pincode'),
                country=request.form.get('country', 'India')
            )
            db.session.add(new_address)
            db.session.flush() # Get new_address.id
            selected_address_id = new_address.id
        else:
            selected_address_id = int(address_id)
            # Verify address belongs to customer
            if not Address.query.filter_by(id=selected_address_id, customer_id=customer.id).first():
                flash('Invalid address selected.', 'error')
                return redirect(url_for('customer.checkout'))

        # Create Order
        order_number = Order.generate_order_number()
        new_order = Order(
            order_number=order_number,
            customer_id=customer.id,
            address_id=selected_address_id,
            subtotal=subtotal,
            shipping_charge=shipping_charge,
            advance_amount=advance_amount,
            remaining_amount=remaining_amount,
            total_amount=total_amount
        )
        db.session.add(new_order)
        db.session.flush()

        # Create OrderItems and clear Cart
        for cart_item in list(cart.items):
            order_item = OrderItem(
                order_id=new_order.id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            db.session.add(order_item)
            db.session.delete(cart_item)

        db.session.commit()
        return redirect(url_for('customer.payment', order_number=new_order.order_number))

    addresses = Address.query.filter_by(customer_id=customer.id).all()
    
    return render_template('customer/checkout.html', 
                           addresses=addresses, 
                           cart_items=cart.items,
                           subtotal=subtotal,
                           shipping=shipping_charge,
                           total=total_amount,
                           advance=advance_amount)

@customer_bp.route('/order/<order_number>/payment', methods=['GET', 'POST'])
@login_required
def payment(order_number):
    """Customer payment submission page and logic."""
    from flask import current_app
    import os
    from datetime import datetime
    from werkzeug.utils import secure_filename
    from app.database.models import Payment

    customer = _get_current_customer()
    order = Order.query.filter_by(order_number=order_number, customer_id=customer.id).first_or_404()
    
    # Determine what type of payment is needed
    if order.payment_status in ('Pending', 'Rejected', 'Pending Verification'):
        payment_type = 'Advance'
        amount = order.advance_amount
    elif order.payment_status in ('Advance Paid', 'Remaining Pending', 'Remaining Pending Verification'):
        payment_type = 'Final'
        amount = order.remaining_amount
    else:
        # Fully Paid
        flash('This order is already fully paid.', 'info')
        return redirect(url_for('customer.my_orders'))

    if request.method == 'POST':
        upi_ref = request.form.get('upi_reference')
        screenshot_file = request.files.get('payment_screenshot')
        
        if not upi_ref:
            flash('UPI Reference ID is required.', 'error')
            return redirect(request.url)
            
        screenshot_filename = None
        if screenshot_file and screenshot_file.filename != '':
            # Validate extension
            ext = os.path.splitext(screenshot_file.filename)[1]
            # Formulate safe unique filename
            timestamp = int(datetime.utcnow().timestamp())
            filename = f"screenshot_{order.order_number}_{payment_type}_{timestamp}{ext}"
            screenshot_filename = secure_filename(filename)
            upload_dir = current_app.config['UPLOAD_FOLDER_PAYMENTS']
            os.makedirs(upload_dir, exist_ok=True)
            upload_path = os.path.join(upload_dir, screenshot_filename)
            screenshot_file.save(upload_path)
        else:
            flash('Payment screenshot is required to verify the transaction.', 'error')
            return redirect(request.url)
            
        # Create or update Payment record
        payment_record = Payment.query.filter_by(order_id=order.id, payment_type=payment_type).first()
        if not payment_record:
            payment_record = Payment(
                order_id=order.id,
                payment_type=payment_type,
                amount=amount
            )
            db.session.add(payment_record)
            
        payment_record.upi_reference = upi_ref
        payment_record.payment_screenshot = screenshot_filename
        payment_record.verified_by_admin = False
        payment_record.status = 'Pending'
        payment_record.created_at = datetime.utcnow()
        payment_record.rejection_reason = None # Clear any previous rejection
        
        # Update order payment status to indicate verification is pending
        if payment_type == 'Advance':
            order.payment_status = 'Pending Verification'
        else:
            order.payment_status = 'Remaining Pending Verification'
            
        db.session.commit()
        return redirect(url_for('customer.payment_success', order_number=order.order_number))
        
    return render_template('customer/payment.html', order=order)

@customer_bp.route('/order/<order_number>/payment/success')
@login_required
def payment_success(order_number):
    """Shows success message after payment submission."""
    customer = _get_current_customer()
    order = Order.query.filter_by(order_number=order_number, customer_id=customer.id).first_or_404()
    return render_template('customer/payment_success.html', order=order)

# ── Informational Pages ──
@customer_bp.route('/about')
def about():
    """Render the About page."""
    return render_template('customer/about.html')

@customer_bp.route('/faq')
def faq():
    """Render the FAQ page."""
    return render_template('customer/faq.html')

@customer_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    """Render the Contact page and handle message submissions."""
    if request.method == 'POST':
        # Collect form data
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        subject = request.form.get('subject')
        message = request.form.get('message')
        # Basic validation
        if not all([name, email, subject, message]):
            flash('All required fields must be filled.', 'error')
            return redirect(url_for('customer.contact'))
        # Store in database
        from app.database.models import ContactMessage
        new_msg = ContactMessage(name=name, email=email, phone=phone, subject=subject, message=message)
        db.session.add(new_msg)
        db.session.commit()
        flash('Your message has been sent. We will get back to you shortly.', 'success')
        return redirect(url_for('customer.contact'))
    return render_template('customer/contact.html')

@customer_bp.route('/custom-order')
def custom_order():
    """Render the Custom Order page."""
    return render_template('customer/custom_order.html')

# ── Cart API Routes (Protected) ──

@customer_bp.route('/cart/add', methods=['POST'])
@login_required
def cart_add():
    data = request.get_json() or {}
    product_identifier = data.get('product_id')
    quantity = int(data.get('quantity', 1))
    
    product = Product.query.filter((Product.slug == str(product_identifier)) | (Product.id == product_identifier)).first()
    
    if not product:
        return jsonify({'success': False, 'message': 'Product not found.'}), 404

    cart = _get_cart()
    
    cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product.id).first()
    if cart_item:
        cart_item.quantity = min(cart_item.quantity + quantity, 10)
    else:
        cart_item = CartItem(cart_id=cart.id, product_id=product.id, quantity=quantity)
        db.session.add(cart_item)
    
    db.session.commit()
    cart_count = sum(i.quantity for i in cart.items)
    return jsonify({'success': True, 'cart_count': cart_count})

@customer_bp.route('/cart/update', methods=['POST'])
@login_required
def cart_update():
    data = request.get_json() or {}
    product_identifier = data.get('product_id')
    quantity = int(data.get('quantity', 1))
    
    cart = _get_cart()
    product = Product.query.filter((Product.slug == str(product_identifier)) | (Product.id == product_identifier)).first()
    
    if product:
        cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product.id).first()
        if cart_item:
            if quantity <= 0:
                db.session.delete(cart_item)
            else:
                cart_item.quantity = min(quantity, 10)
            db.session.commit()
            
    cart_count = sum(i.quantity for i in cart.items) if cart else 0
    return jsonify({'success': True, 'cart_count': cart_count})

@customer_bp.route('/cart/remove', methods=['POST'])
@login_required
def cart_remove():
    data = request.get_json() or {}
    product_identifier = data.get('product_id')
    
    cart = _get_cart()
    product = Product.query.filter((Product.slug == str(product_identifier)) | (Product.id == product_identifier)).first()
    
    if product:
        cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product.id).first()
        if cart_item:
            db.session.delete(cart_item)
            db.session.commit()
            
    cart_count = sum(i.quantity for i in cart.items) if cart else 0
    return jsonify({'success': True, 'cart_count': cart_count})

@customer_bp.route('/cart/count')
def cart_count():
    if 'customer_id' not in session:
        return jsonify({'cart_count': 0})
        
    cart = _get_cart()
    if not cart:
        return jsonify({'cart_count': 0})
        
    cart_count = sum(i.quantity for i in cart.items)
    return jsonify({'cart_count': cart_count})

@customer_bp.route('/my-orders')
@login_required
def my_orders():
    from app.database.models import Order
    customer = _get_current_customer()
    orders = Order.query.filter_by(customer_id=customer.id).order_by(Order.created_at.desc()).all()
    return render_template('customer/my_orders.html', orders=orders)


@customer_bp.route('/my-orders/<order_number>')
@login_required
def order_detail(order_number):
    """Customer order detail + tracking page.
    Only the owning customer may access this view.
    """
    from app.database.models import Order
    customer = _get_current_customer()
    order = Order.query.filter_by(order_number=order_number).first_or_404()

    # Ownership check - 403 if this order belongs to someone else
    if order.customer_id != customer.id:
        from flask import abort
        abort(403)

    # Compute tracking stage (0-indexed, 0..5)
    # Stages:
    #   0  Order Placed       - always done once order exists
    #   1  Payment Verified   - payment_status in ('Advance Paid', 'Fully Paid')
    #   2  Production Started - production_status in ('Started', 'Completed')
    #   3  Completed          - production_status == 'Completed'
    #   4  Dispatched         - order_status in ('Dispatched', 'Delivered')
    #   5  Delivered          - order_status == 'Delivered'

    ps  = order.payment_status
    prs = order.production_status
    os  = order.order_status

    if os == 'Delivered':
        stage = 5
    elif os == 'Dispatched':
        stage = 4
    elif prs == 'Completed':
        stage = 3
    elif prs == 'Started':
        stage = 2
    elif ps in ('Advance Paid', 'Fully Paid'):
        stage = 1
    else:
        stage = 0

    tracking_stages = [
        {'label': 'Order Placed',       'desc': 'Your order has been received.'},
        {'label': 'Payment Verified',   'desc': 'Advance payment confirmed by Mithra.'},
        {'label': 'Production Started', 'desc': 'Crocheting has begun — made just for you.'},
        {'label': 'Completed',          'desc': 'Your creation is finished and quality-checked.'},
        {'label': 'Dispatched',         'desc': 'Handed to courier and on its way.'},
        {'label': 'Delivered',          'desc': 'Arrived with love. Enjoy your piece!'},
    ]

    return render_template(
        'customer/order_detail.html',
        order=order,
        tracking_stages=tracking_stages,
        current_stage=stage,
    )

@customer_bp.route('/product/<slug>/review', methods=['POST'])
@login_required
def submit_review(slug):
    from app.database.models import Product, Review, Order, OrderItem
    product = Product.query.filter_by(slug=slug).first_or_404()
    customer = _get_current_customer()
    
    # Check if already reviewed
    existing_review = Review.query.filter_by(customer_id=customer.id, product_id=product.id).first()
    if existing_review:
        flash('You have already reviewed this product.', 'error')
        return redirect(url_for('customer.product', slug=slug))
        
    # Check if they have a delivered order with this product
    delivered_order = Order.query.join(OrderItem).filter(
        Order.customer_id == customer.id,
        Order.order_status == 'Delivered',
        OrderItem.product_id == product.id
    ).first()
    
    if not delivered_order:
        flash('You can only review products you have purchased and received.', 'error')
        return redirect(url_for('customer.product', slug=slug))
        
    rating = request.form.get('rating')
    comment = request.form.get('comment')
    
    if not rating:
        flash('Rating is required.', 'error')
        return redirect(url_for('customer.product', slug=slug))
        
    try:
        rating_val = int(rating)
        if rating_val < 1 or rating_val > 5:
            raise ValueError()
    except ValueError:
        flash('Invalid rating value.', 'error')
        return redirect(url_for('customer.product', slug=slug))
        
    new_review = Review(
        customer_id=customer.id,
        product_id=product.id,
        rating=rating_val,
        comment=comment,
        approved=True # Set to True directly so customers can see their reviews instantly on submission
    )
    db.session.add(new_review)
    db.session.commit()
    
    flash('Thank you! Your review has been submitted successfully.', 'success')
    return redirect(url_for('customer.product', slug=slug))
