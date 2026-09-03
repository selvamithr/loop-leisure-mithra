import os, re
BASE_DIR = r'c:/Users/sasi6/OneDrive/Desktop/loop & leisure ~mithra'
with open(os.path.join(BASE_DIR, 'app/templates/admin/orders.html'), 'r', encoding='utf-8') as f:
    content = f.read()

# Extract everything before <main class="admin-main">
header_split = content.split('<main class="admin-main">')
header = header_split[0] + '<main class="admin-main">\n'

# Update title and nav active states
header = header.replace('<title>All Orders | Admin Dashboard | Loop & Leisure</title>', '<title>Products | Admin Dashboard | Loop & Leisure</title>')
header = header.replace('class="admin-nav-item active">Orders</a>', 'class="admin-nav-item">Orders</a>')
# Ensure Products is active
header = re.sub(r'<a href="\{\{ url_for\(\'admin\.admin_products\'\).*?>Products</a>', '<a href="{{ url_for(\'admin.admin_products\') }}" class="admin-nav-item active">Products</a>', header)

products_main = '''
        <div class="admin-header">
            <div class="admin-header-title">
                <h1>Products</h1>
                <p>Manage catalog, pricing, and stock.</p>
            </div>
            <div class="admin-header-actions">
                <a href="{{ url_for('admin.product_add') }}" class="btn btn-primary">Add Product</a>
            </div>
        </div>

        <!-- Flash Messages -->
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category if category != 'error' else 'danger' }}" style="margin-bottom: 1.5rem; padding: 1rem; border-radius: 6px; background: {% if category == 'success' %}#e8f5e9; color: #2e7d32; border: 1px solid #c8e6c9{% else %}#ffebee; color: #c62828; border: 1px solid #ffcdd2{% endif %};">
                        {{ message }}
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        <div class="admin-card">
            <div style="padding: 1.5rem; border-bottom: 1px solid #e2e8f0; display: flex; justify-content: space-between; align-items: center;">
                <h2 style="margin: 0; font-size: 1.125rem; color: #0f172a;">All Products</h2>
            </div>
            
            <div class="admin-table-container">
                <table class="admin-table">
                    <thead>
                        <tr>
                            <th>Product Name</th>
                            <th>Category</th>
                            <th>Price</th>
                            <th>Stock Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for product in products %}
                        <tr>
                            <td style="font-weight: 500; color: #0f172a;">{{ product.name }}</td>
                            <td><span style="background: #f1f5f9; padding: 4px 8px; border-radius: 4px; font-size: 0.75rem; text-transform: uppercase; font-weight: 600;">{{ product.category }}</span></td>
                            <td>&#8377;{{ '%.2f' % product.price }}</td>
                            <td>
                                {% if product.stock_status == 'available' %}
                                    <span style="color: #10b981; font-weight: 500;">Available</span>
                                {% elif product.stock_status == 'out_of_stock' %}
                                    <span style="color: #ef4444; font-weight: 500;">Out of Stock</span>
                                {% else %}
                                    <span style="color: #64748b; font-weight: 500;">{{ product.stock_status|capitalize }}</span>
                                {% endif %}
                            </td>
                            <td>
                                <a href="{{ url_for('admin.product_edit', product_id=product.id) }}" class="btn btn-secondary btn-sm">Edit</a>
                                <form action="{{ url_for('admin.product_delete', product_id=product.id) }}" method="POST" style="display: inline-block;" onsubmit="return confirm('Are you sure you want to delete this product? It will be archived to preserve historical orders.');">
                                    <button type="submit" class="btn btn-primary btn-sm" style="background-color: #ef4444; border-color: #ef4444;">Delete</button>
                                </form>
                            </td>
                        </tr>
                        {% else %}
                        <tr>
                            <td colspan="5" style="text-align: center; padding: 2rem; color: #64748b;">No active products found.</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </main>
</div>
</body>
</html>
'''

with open(os.path.join(BASE_DIR, 'app/templates/admin/products.html'), 'w', encoding='utf-8') as f:
    f.write(header + products_main)
print("Created products.html")
