import os
import sys

BASE_DIR = r'c:/Users/sasi6/OneDrive/Desktop/loop & leisure ~mithra'
sys.path.insert(0, BASE_DIR)

from app import create_app
from app.database import db
from app.database.models import Customer, Product, Order, Payment

def run_test():
    app = create_app()
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        with app.app_context():
            # 1. Login
            client.post('/login', data={'email': 'testuser@example.com', 'password': 'password123'})
            
            # 2. Add to cart
            product = Product.query.first()
            if not product:
                print("No products available.")
                return
            client.post('/cart/add', json={'product_id': product.id, 'quantity': 1})
            
            # 3. Checkout
            resp = client.post('/checkout', data={
                'address_id': 'new',
                'name': 'Test User',
                'phone': '9876543210',
                'address_line1': '123 Test St',
                'city': 'Test City',
                'state': 'Test State',
                'pincode': '123456',
                'country': 'India',
                'payment_method': 'upi'
            }, follow_redirects=True)
            
            html = resp.data.decode('utf-8')
            
            # Find order number
            import re
            order_number = None
            if 'Advance Payment Required (50%)' in html:
                match = re.search(r'order (ORD-[A-Z0-9]+)', html)
                if match:
                    order_number = match.group(1)
                    
            if not order_number:
                order = Order.query.order_by(Order.id.desc()).first()
                order_number = order.order_number
                
            print(f"Order created: {order_number}")
            
            # 4. Check Payment Page
            resp = client.get(f'/order/{order_number}/payment')
            html = resp.data.decode('utf-8')
            if 'Advance Payment Required' in html and '&#8377;' in html:
                print("  - OK: 50% advance shown correctly")
            else:
                print("  - FAIL: Advance amount display issue")
                import sys
                print("HTML content excerpt:", html, file=sys.stderr)
                
            # 5. Submit Payment
            import io
            data = {
                'upi_reference': 'TXN123456789',
                'payment_screenshot': (io.BytesIO(b"fake image data"), 'screenshot.png')
            }
            resp = client.post(f'/order/{order_number}/payment', data=data, content_type='multipart/form-data', follow_redirects=True)
            if b'awaiting verification' in resp.data.lower() or b'submitted successfully' in resp.data.lower():
                print("  - OK: Success message shown to customer")
            else:
                print("  - FAIL: Success message not found")
                import sys
                with open('payment_fail_debug.html', 'w', encoding='utf-8') as f:
                    f.write(resp.data.decode('utf-8'))
                
            # 6. Admin Login
            client.get('/admin/logout')
            client.post('/admin/login', data={'email': 'admin@loopandleisure.com', 'password': 'admin123'})
            
            # 7. Admin Checks Order
            resp = client.get(f'/admin/orders/{order_number}')
            html = resp.data.decode('utf-8')
            if 'TXN123456789' in html and 'screenshot.png' in html:
                print("  - OK: Admin sees transaction ID and screenshot")
            else:
                print("  - FAIL: Admin doesn't see payment details")
                
            # Extract payment ID
            pmatch = re.search(rf'/admin/order/{order_number}/payment/(\d+)/verify', html)
            if pmatch:
                payment_id = pmatch.group(1)
                
                # 8. Admin Approves Payment
                resp = client.post(f'/admin/order/{order_number}/payment/{payment_id}/verify', data={}, follow_redirects=True)
                if b'verified successfully' in resp.data.lower():
                    print("  - OK: Payment verified message shown to admin")
                else:
                    print("  - FAIL: Payment verified message not found")
            else:
                print("  - FAIL: Could not extract payment ID for verification")
                
            # 9. Customer Checks Tracking
            client.get('/logout')
            client.post('/login', data={'email': 'testuser@example.com', 'password': 'password123'})
            resp = client.get(f'/my-orders/{order_number}')
            if b'Advance Paid' in resp.data or b'Payment Verified' in resp.data:
                print("  - OK: Customer sees payment verified in tracking")
            else:
                print("  - FAIL: Customer tracking status not updated")

run_test()
