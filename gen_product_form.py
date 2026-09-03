import os, re
BASE_DIR = r'c:/Users/sasi6/OneDrive/Desktop/loop & leisure ~mithra'
with open(os.path.join(BASE_DIR, 'app/templates/admin/orders.html'), 'r', encoding='utf-8') as f:
    content = f.read()

# Extract header
header_split = content.split('<main class="admin-main">')
header = header_split[0] + '<main class="admin-main">\n'

header = header.replace('<title>All Orders | Admin Dashboard | Loop & Leisure</title>', '<title>{% if product %}Edit{% else %}Add{% endif %} Product | Admin Dashboard | Loop & Leisure</title>')
header = header.replace('class="admin-nav-item active">Orders</a>', 'class="admin-nav-item">Orders</a>')
header = re.sub(r'<a href="\{\{ url_for\(\'admin\.admin_products\'\).*?>Products</a>', '<a href="{{ url_for(\'admin.admin_products\') }}" class="admin-nav-item active">Products</a>', header)

form_main = '''
        <div class="admin-header">
            <div class="admin-header-title">
                <h1>{% if product %}Edit Product{% else %}Add New Product{% endif %}</h1>
                <p>{% if product %}Update details for {{ product.name }}.{% else %}Create a new product for the catalog.{% endif %}</p>
            </div>
            <div class="admin-header-actions">
                <a href="{{ url_for('admin.admin_products') }}" class="btn btn-secondary">Cancel</a>
            </div>
        </div>

        <div class="admin-card" style="max-width: 800px;">
            <div style="padding: 1.5rem; border-bottom: 1px solid #e2e8f0;">
                <h2 style="margin: 0; font-size: 1.125rem; color: #0f172a;">Product Details</h2>
            </div>
            <div style="padding: 1.5rem;">
                <form method="POST" action="{{ url_for('admin.product_edit', product_id=product.id) if product else url_for('admin.product_add') }}">
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-bottom: 1.5rem;">
                        <!-- Name -->
                        <div style="grid-column: 1 / -1;">
                            <label style="display: block; font-size: 0.875rem; font-weight: 500; color: #334155; margin-bottom: 0.5rem;">Product Name</label>
                            <input type="text" name="name" required value="{{ product.name if product else '' }}" style="width: 100%; padding: 0.625rem; border: 1px solid #cbd5e1; border-radius: 4px; font-family: 'Inter', sans-serif;">
                        </div>

                        <!-- Slug -->
                        <div style="grid-column: 1 / -1;">
                            <label style="display: block; font-size: 0.875rem; font-weight: 500; color: #334155; margin-bottom: 0.5rem;">Slug (URL friendly name)</label>
                            <input type="text" name="slug" value="{{ product.slug if product else '' }}" placeholder="Leave blank to auto-generate" style="width: 100%; padding: 0.625rem; border: 1px solid #cbd5e1; border-radius: 4px; font-family: 'Inter', sans-serif;">
                            <p style="font-size: 0.75rem; color: #64748b; margin-top: 0.25rem;">e.g., crochet-rose-bouquet</p>
                        </div>

                        <!-- Category -->
                        <div>
                            <label style="display: block; font-size: 0.875rem; font-weight: 500; color: #334155; margin-bottom: 0.5rem;">Category</label>
                            <select name="category" required style="width: 100%; padding: 0.625rem; border: 1px solid #cbd5e1; border-radius: 4px; font-family: 'Inter', sans-serif; background: #fff;">
                                <option value="bouquets" {% if product and product.category == 'bouquets' %}selected{% endif %}>Bouquets</option>
                                <option value="keychains" {% if product and product.category == 'keychains' %}selected{% endif %}>Keychains</option>
                                <option value="amigurumi" {% if product and product.category == 'amigurumi' %}selected{% endif %}>Amigurumi</option>
                                <option value="accessories" {% if product and product.category == 'accessories' %}selected{% endif %}>Accessories</option>
                            </select>
                        </div>

                        <!-- Price -->
                        <div>
                            <label style="display: block; font-size: 0.875rem; font-weight: 500; color: #334155; margin-bottom: 0.5rem;">Price (&#8377;)</label>
                            <input type="number" step="0.01" name="price" required value="{{ product.price if product else '' }}" style="width: 100%; padding: 0.625rem; border: 1px solid #cbd5e1; border-radius: 4px; font-family: 'Inter', sans-serif;">
                        </div>

                        <!-- Stock Status -->
                        <div>
                            <label style="display: block; font-size: 0.875rem; font-weight: 500; color: #334155; margin-bottom: 0.5rem;">Stock Status</label>
                            <select name="stock_status" style="width: 100%; padding: 0.625rem; border: 1px solid #cbd5e1; border-radius: 4px; font-family: 'Inter', sans-serif; background: #fff;">
                                <option value="available" {% if product and product.stock_status == 'available' %}selected{% endif %}>Available</option>
                                <option value="out_of_stock" {% if product and product.stock_status == 'out_of_stock' %}selected{% endif %}>Out of Stock</option>
                                <option value="archived" {% if product and product.stock_status == 'archived' %}selected{% endif %}>Archived (Hidden)</option>
                            </select>
                        </div>
                        
                        <!-- Description -->
                        <div style="grid-column: 1 / -1;">
                            <label style="display: block; font-size: 0.875rem; font-weight: 500; color: #334155; margin-bottom: 0.5rem;">Description</label>
                            <textarea name="description" rows="5" style="width: 100%; padding: 0.625rem; border: 1px solid #cbd5e1; border-radius: 4px; font-family: 'Inter', sans-serif; resize: vertical;">{{ product.description if product else '' }}</textarea>
                        </div>
                    </div>
                    
                    <div style="border-top: 1px solid #e2e8f0; padding-top: 1.5rem; display: flex; justify-content: flex-end;">
                        <button type="submit" class="btn btn-primary">{% if product %}Save Changes{% else %}Create Product{% endif %}</button>
                    </div>
                </form>
            </div>
        </div>
    </main>
</div>
</body>
</html>
'''

with open(os.path.join(BASE_DIR, 'app/templates/admin/product_form.html'), 'w', encoding='utf-8') as f:
    f.write(header + form_main)
print("Created product_form.html")
