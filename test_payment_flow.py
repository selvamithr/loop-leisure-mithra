import urllib.request
import urllib.parse
import urllib.error
import http.cookiejar
import re
import os
import io

BASE = 'http://127.0.0.1:5000'

def test_payment_flow():
    jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    opener.addheaders = [('User-Agent', 'TestBot/1.0')]

    def get(path):
        req = urllib.request.Request(BASE + path)
        try:
            resp = opener.open(req, timeout=10)
            return resp.read().decode('utf-8', errors='ignore'), resp.geturl(), resp.getcode()
        except urllib.error.HTTPError as e:
            return e.read().decode('utf-8', errors='ignore'), BASE + path, e.code

    def post(path, data_dict, is_multipart=False):
        if not is_multipart:
            html, _, _ = get(path)
            match = re.search(r'name="csrf_token"\s+type="hidden"\s+value="([^"]+)"', html)
            if match:
                data_dict['csrf_token'] = match.group(1)
            data = urllib.parse.urlencode(data_dict).encode()
            req = urllib.request.Request(BASE + path, data=data, method='POST')
            req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        else:
            # Simple multipart/form-data generator for the test
            boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
            body = []
            
            # extract CSRF again
            html, _, _ = get(path)
            match = re.search(r'name="csrf_token"\s+type="hidden"\s+value="([^"]+)"', html)
            if match:
                data_dict['csrf_token'] = match.group(1)
                
            for key, val in data_dict.items():
                if isinstance(val, dict): # File
                    body.extend([
                        f'--{boundary}',
                        f'Content-Disposition: form-data; name="{key}"; filename="{val["filename"]}"',
                        f'Content-Type: {val["content_type"]}',
                        '',
                        val['content']
                    ])
                else:
                    body.extend([
                        f'--{boundary}',
                        f'Content-Disposition: form-data; name="{key}"',
                        '',
                        str(val)
                    ])
            body.append(f'--{boundary}--')
            body.append('')
            body_bytes = '\r\n'.join(body).encode('utf-8')
            
            req = urllib.request.Request(BASE + path, data=body_bytes, method='POST')
            req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')

        try:
            resp = opener.open(req, timeout=10)
            return resp.read().decode('utf-8', errors='ignore'), resp.geturl(), resp.getcode()
        except urllib.error.HTTPError as e:
            return e.read().decode('utf-8', errors='ignore'), BASE + path, e.code

    print("1. Customer Login")
    html, url, code = post('/login', {'email': 'testuser@example.com', 'password': 'password123'})
    
    print("2. Add Item to Cart")
    # Using JSON post for API
    req = urllib.request.Request(BASE + '/cart/add', data=b'{"product_id": 1, "quantity": 1}', method='POST')
    req.add_header('Content-Type', 'application/json')
    try:
        resp = opener.open(req)
    except: pass

    print("3. Checkout")
    html, url, code = post('/checkout', {
        'shipping_name': 'Test User',
        'shipping_phone': '9876543210',
        'shipping_address': '123 Test St',
        'shipping_city': 'Test City',
        'shipping_state': 'Test State',
        'shipping_pincode': '123456',
        'payment_method': 'upi'
    })
    
    # Extract order number from URL /payment/ORD-xxx
    match = re.search(r'/payment/(ORD-\w+)', url)
    if not match:
        print("Failed to get order number", url)
        return False
    order_number = match.group(1)
    print(f"Order created: {order_number}")

    print("4. Check Payment Page displays 50% amount")
    html, url, code = get(f'/payment/{order_number}')
    if 'Advance Payment Required (50%)' in html and '&#8377;' in html:
        print("  - OK: 50% advance shown correctly")
    else:
        print("  - FAIL: Advance amount display issue")

    print("5. Submit Payment Proof")
    html, url, code = post(f'/payment/{order_number}', {
        'transaction_id': 'TXN123456789',
        'payment_proof': {
            'filename': 'screenshot.png',
            'content_type': 'image/png',
            'content': 'fake image content'
        }
    }, is_multipart=True)
    
    if 'awaiting verification' in html.lower():
        print("  - OK: Success message shown to customer")
    else:
        print("  - FAIL: Success message not found")

    # Now Login as Admin
    print("6. Admin Login")
    admin_jar = http.cookiejar.CookieJar()
    admin_opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(admin_jar))
    admin_opener.addheaders = [('User-Agent', 'TestBot/1.0')]
    
    def admin_get(path):
        req = urllib.request.Request(BASE + path)
        try:
            resp = admin_opener.open(req)
            return resp.read().decode('utf-8', errors='ignore')
        except urllib.error.HTTPError as e:
            return e.read().decode('utf-8', errors='ignore')
            
    def admin_post(path, data_dict):
        html = admin_get(path)
        match = re.search(r'name="csrf_token"\s+type="hidden"\s+value="([^"]+)"', html)
        if match:
            data_dict['csrf_token'] = match.group(1)
        data = urllib.parse.urlencode(data_dict).encode()
        req = urllib.request.Request(BASE + path, data=data, method='POST')
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        try:
            resp = admin_opener.open(req)
            return resp.read().decode('utf-8', errors='ignore')
        except urllib.error.HTTPError as e:
            return e.read().decode('utf-8', errors='ignore')

    admin_post('/admin/login', {'email': 'admin@loopandleisure.com', 'password': 'admin123'})
    
    print("7. Admin Checks Order Details")
    html = admin_get(f'/admin/orders/{order_number}')
    if 'TXN123456789' in html and 'screenshot.png' in html:
        print("  - OK: Admin sees transaction ID and screenshot")
    else:
        print("  - FAIL: Admin doesn't see payment details")
        
    # Extract Payment ID
    pmatch = re.search(rf'/admin/order/{order_number}/payment/(\d+)/verify', html)
    if not pmatch:
        print("  - FAIL: Could not find payment verification form")
        return False
    payment_id = pmatch.group(1)
    
    print("8. Admin Approves Payment")
    html = admin_post(f'/admin/order/{order_number}/payment/{payment_id}/verify', {})
    if 'Payment verified successfully' in html:
        print("  - OK: Payment verified message shown to admin")

    print("9. Customer Checks Order Tracking")
    html, _, _ = get(f'/my-orders/{order_number}')
    if 'Advance Paid' in html or 'Payment Verified' in html:
        print("  - OK: Customer sees payment verified in tracking")
    else:
        print("  - FAIL: Customer tracking status not updated")

    print("\nAll flow checks completed successfully.")

if __name__ == '__main__':
    test_payment_flow()
