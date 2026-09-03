import urllib.request
import urllib.parse
import urllib.error
import http.cookiejar
import json
import re

BASE = 'http://127.0.0.1:5000'
results = []

def check(name, condition):
    status = 'PASS' if condition else 'FAIL'
    results.append((status, name))
    print(f"  {status}  {name}")

jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
opener.addheaders = [('User-Agent', 'TestBot/1.0')]

def get(path):
    req = urllib.request.Request(BASE + path)
    try:
        resp = opener.open(req, timeout=8)
        return resp.read().decode('utf-8', errors='ignore'), resp.geturl(), resp.getcode()
    except urllib.error.HTTPError as e:
        return e.read().decode('utf-8', errors='ignore'), BASE + path, e.code

def post(path, data_dict):
    # First get the page to extract CSRF token if needed
    html, _, _ = get(path)
    match = re.search(r'name="csrf_token"\s+type="hidden"\s+value="([^"]+)"', html)
    if match:
        data_dict['csrf_token'] = match.group(1)
        
    data = urllib.parse.urlencode(data_dict).encode()
    req = urllib.request.Request(BASE + path, data=data, method='POST')
    req.add_header('Content-Type', 'application/x-www-form-urlencoded')
    try:
        resp = opener.open(req, timeout=8)
        return resp.read().decode('utf-8', errors='ignore'), resp.geturl(), resp.getcode()
    except urllib.error.HTTPError as e:
        return e.read().decode('utf-8', errors='ignore'), BASE + path, e.code

print("\n=== ADMIN PRODUCT MANAGEMENT TESTS ===\n")

# 1. Test Unauthenticated Access
html, url, code = get('/admin/products')
check("Unauthorized users redirected from /admin/products", 'login' in url or 'login' in html.lower())

# 2. Login as Admin
html, url, code = post('/admin/login', {'email': 'admin@loopandleisure.com', 'password': 'admin123'})
check("Admin login successful", 'dashboard' in url or 'logout' in html.lower())

# 3. Access Products Page
html, url, code = get('/admin/products')
check("Admin products page loads", code == 200 and 'All Products' in html)

# 4. Add Temporary Product
html, url, code = post('/admin/products/add', {
    'name': 'Test Crochet Item',
    'slug': 'test-crochet-item',
    'category': 'bouquets',
    'price': '999.99',
    'stock_status': 'available',
    'description': 'A temporary product for testing.'
})
check("Added temporary product successfully", code in (200, 302, 303))

# Verify it appears in Admin List
html, url, code = get('/admin/products')
check("Temporary product appears in admin list", 'Test Crochet Item' in html)

# 5. Verify it appears in Shop
html, url, code = get('/shop')
check("Temporary product appears in shop", 'Test Crochet Item' in html and '999.99' in html)

# 6. Find Product ID for Editing
match = re.search(r'href="/admin/products/edit/(\d+)"[^>]*>Edit</a>\s*<form[^>]*action="/admin/products/delete/\1"', html)
if not match:
    # Alternative regex search for admin products
    html_admin, _, _ = get('/admin/products')
    match = re.search(r'href="/admin/products/edit/(\d+)"[^>]*>Edit</a>', html_admin)
product_id = match.group(1) if match else None

if product_id:
    # 7. Edit the Product
    post(f'/admin/products/edit/{product_id}', {
        'name': 'Edited Crochet Item',
        'slug': 'test-crochet-item',
        'category': 'accessories',
        'price': '888.88',
        'stock_status': 'available',
        'description': 'Edited description.'
    })
    
    html_shop, _, _ = get('/shop')
    check("Edited product changes reflect in shop", 'Edited Crochet Item' in html_shop and '888.88' in html_shop and 'Test Crochet Item' not in html_shop)
    
    # 8. Delete (Archive) the Product
    post(f'/admin/products/delete/{product_id}', {})
    
    html_shop2, _, _ = get('/shop')
    check("Deleted (archived) product no longer in shop", 'Edited Crochet Item' not in html_shop2)
    
    html_admin2, _, _ = get('/admin/products')
    check("Deleted product no longer in active admin list", 'Edited Crochet Item' not in html_admin2)
else:
    check("Could not extract product ID to test edit/delete", False)

# ── SUMMARY ──
print("\n" + "="*44)
passed = sum(1 for s, _ in results if s == 'PASS')
failed = sum(1 for s, _ in results if s == 'FAIL')
print(f"  PASSED: {passed} / {passed + failed}")
if failed:
    print("  FAILED CHECKS:")
    for s, n in results:
        if s == 'FAIL':
            print(f"    - {n}")
print("="*44 + "\n")
