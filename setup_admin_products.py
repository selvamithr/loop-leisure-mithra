import os
import re

BASE_DIR = r'c:/Users/sasi6/OneDrive/Desktop/loop & leisure ~mithra'

def inject_admin_routes():
    routes_path = os.path.join(BASE_DIR, 'app/admin/routes.py')
    with open(routes_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'def admin_products():' in content:
        print("Admin products routes already exist.")
        return

    new_routes = """
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
"""
    # Inject before contact messages
    target = "# ── Admin Contact Messages ──"
    if target in content:
        content = content.replace(target, new_routes + '\n' + target)
        with open(routes_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Injected admin product routes.")
    else:
        with open(routes_path, 'a', encoding='utf-8') as f:
            f.write(new_routes)
        print("Appended admin product routes.")

def update_shop_route():
    routes_path = os.path.join(BASE_DIR, 'app/customer/routes.py')
    with open(routes_path, 'r', encoding='utf-8') as f:
        content = f.read()

    old_shop = """@customer_bp.route('/shop')
def shop():
    return render_template('customer/shop.html')"""
    
    new_shop = """@customer_bp.route('/shop')
def shop():
    from app.database.models import Product
    products = Product.query.filter(Product.stock_status != 'archived').order_by(Product.created_at.desc()).all()
    return render_template('customer/shop.html', products=products)"""

    if old_shop in content:
        content = content.replace(old_shop, new_shop)
        with open(routes_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Updated /shop route in customer/routes.py")
    else:
        print("Could not find the exact old_shop block. Let's try regex.")
        content = re.sub(r"@customer_bp\.route\('/shop'\)\ndef shop\(\):\n\s+return render_template\('customer/shop\.html'\)", new_shop, content)
        with open(routes_path, 'w', encoding='utf-8') as f:
            f.write(content)

def update_admin_navs():
    templates_dir = os.path.join(BASE_DIR, 'app/templates/admin')
    nav_item = """<a href="{{ url_for('admin.admin_products') }}" class="admin-nav-item{% if request.endpoint in ('admin.admin_products', 'admin.product_add', 'admin.product_edit') %} active{% endif %}">Products</a>"""
    
    for filename in os.listdir(templates_dir):
        if not filename.endswith('.html'): continue
        filepath = os.path.join(templates_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'admin.admin_products' in content:
            continue
            
        # Insert before logout link
        pattern = r'(<a href="\{\{ url_for\(\'admin\.logout\'\).*?>Logout</a>)'
        if re.search(pattern, content):
            content = re.sub(pattern, f"{nav_item}\n                \\1", content)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated nav in {filename}")

def update_shop_template():
    shop_path = os.path.join(BASE_DIR, 'app/templates/customer/shop.html')
    with open(shop_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    start_marker = '<div class="shop-grid" id="shopGrid">'
    end_marker = '</div>\n        </div>\n    </section>'
    
    if start_marker in content and end_marker in content:
        start_idx = content.find(start_marker) + len(start_marker)
        end_idx = content.find(end_marker)
        
        dynamic_grid = """
                {% for product in products %}
                <div class="shop-product-card" data-category="{{ product.category|lower }}">
                    <div class="shop-product-img-wrap">
                        {% if product.images and product.images|length > 0 %}
                            <img src="{{ product.images[0].image_path }}" alt="{{ product.name }}" class="shop-product-img" loading="lazy">
                        {% else %}
                            <img src="https://picsum.photos/seed/{{ product.slug }}/500/600" alt="{{ product.name }}" class="shop-product-img" loading="lazy">
                        {% endif %}
                    </div>
                    <div class="shop-product-info">
                        <div class="shop-product-rating" aria-label="5 out of 5 stars">★★★★★</div>
                        <h3 class="shop-product-title">{{ product.name }}</h3>
                        <div class="shop-product-category">{{ product.category|capitalize }}</div>
                        <div class="shop-product-price">&#8377;{{ '%.2f' % product.price }}</div>
                        <a href="{{ url_for('customer.product', slug=product.slug) }}" class="btn btn-primary shop-product-btn">View Product</a>
                    </div>
                </div>
                {% endfor %}
                """
        new_content = content[:start_idx] + dynamic_grid + content[end_idx:]
        with open(shop_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Updated shop.html with dynamic products.")
    else:
        print("Could not find markers in shop.html.")

inject_admin_routes()
update_shop_route()
update_admin_navs()
update_shop_template()
