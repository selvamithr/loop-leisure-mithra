import os
import sys
import io
import re

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
            # 1. Login as Customer
            client.post('/login', data={'email': 'testuser@example.com', 'password': 'password123'})
            
            # Setup an order with 50% advance verified
            customer = Customer.query.filter_by(email='testuser@example.com').first()
            product = Product.query.first()
            
            # Add to cart & Checkout
            client.post('/cart/add', json={'product_id': product.id, 'quantity': 1})
            client.post('/checkout', data={
                'address_id': 'new', 'name': 'Test User', 'phone': '9876543210',
                'address_line1': '123 Test St', 'city': 'Test City', 'state': 'Test State',
                'pincode': '123456', 'country': 'India', 'payment_method': 'upi'
            }, follow_redirects=True)
            
            order = Order.query.filter_by(customer_id=customer.id).order_by(Order.id.desc()).first()
            order_number = order.order_number
            print(f"1. Created order {order_number} and verifying advance payment.")
            
            # Admin login & verify advance
            client.get('/logout')
            client.post('/admin/login', data={'email': 'admin@loopandleisure.com', 'password': 'admin123'})
            # We mock the advance payment process directly in DB for speed
            order.payment_status = 'Advance Paid'
            order.order_status = 'Confirmed'
            order.production_status = 'Started'
            db.session.commit()
            
            # 2 & 3. Login as Customer, check balance amount & availability
            client.get('/admin/logout')
            client.post('/login', data={'email': 'testuser@example.com', 'password': 'password123'})
            
            resp = client.get(f'/my-orders/{order_number}')
            html = resp.data.decode('utf-8')
            
            if 'Advance Paid' in html and f"&#8377;{order.remaining_amount:.2f}" in html:
                print("2. Confirm balance amount is correct: OK")
            else:
                print("2. Confirm balance amount is correct: FAIL")
                
            if 'Balance payment will be collected before/at dispatch' in html and 'Pay Balance' not in html:
                print("3. Confirm balance payment is NOT available before appropriate stage: OK")
            else:
                print("3. Confirm balance payment is NOT available before appropriate stage: FAIL")
                
            # 4. Move order to completed stage (Admin)
            client.get('/logout')
            client.post('/admin/login', data={'email': 'admin@loopandleisure.com', 'password': 'admin123'})
            client.post(f'/admin/order/{order_number}/production', data={'production_status': 'Completed'})
            client.post(f'/admin/order/{order_number}/request-remaining', data={})
            print("4. Moved order to Completed and Requested Final Payment")
            
            # 5. Confirm Pay Balance appears
            client.get('/admin/logout')
            client.post('/login', data={'email': 'testuser@example.com', 'password': 'password123'})
            resp = client.get(f'/my-orders/{order_number}')
            html = resp.data.decode('utf-8')
            if 'Pay Balance' in html:
                print("5. Confirm Pay Balance appears for customer: OK")
            else:
                print("5. Confirm Pay Balance appears for customer: FAIL")
                
            # 6 & 7. Submit final payment proof
            data = {
                'upi_reference': 'FINALTXN999',
                'payment_screenshot': (io.BytesIO(b"final fake image"), 'final_screenshot.png')
            }
            resp = client.post(f'/order/{order_number}/payment', data=data, content_type='multipart/form-data', follow_redirects=True)
            
            # Check DB status
            db.session.refresh(order)
            if order.payment_status == 'Remaining Pending Verification':
                print("6 & 7. Submit final payment proof & Status becomes Pending Verification: OK")
            else:
                print(f"6 & 7. Submit final payment proof: FAIL (Status: {order.payment_status})")
                
            # 8, 9 & 10. Admin verifies final payment
            client.get('/logout')
            client.post('/admin/login', data={'email': 'admin@loopandleisure.com', 'password': 'admin123'})
            
            payment = Payment.query.filter_by(order_id=order.id, payment_type='Final').first()
            if payment and payment.status == 'Pending':
                client.post(f'/admin/order/{order_number}/payment/{payment.id}/verify', data={}, follow_redirects=True)
                db.session.refresh(order)
                if order.payment_status == 'Fully Paid':
                    print("8, 9, 10. Admin verifies final payment: OK")
                else:
                    print("8, 9, 10. Admin verifies final payment: FAIL")
            else:
                print("Admin payment fetch FAIL")
                
            # 11, 12, 13, 14, 15. Customer checks order tracking
            client.get('/admin/logout')
            client.post('/login', data={'email': 'testuser@example.com', 'password': 'password123'})
            resp = client.get(f'/my-orders/{order_number}')
            html = resp.data.decode('utf-8')
            
            if 'Fully Paid' in html:
                print("12. Confirm Balance Paid/Verified: OK")
            else:
                print("12. Confirm Balance Paid/Verified: FAIL")
                
            if '&#8377;0.00' in html and 'Balance Due' in html:
                print("13. Confirm Balance Due becomes ₹0: OK")
            else:
                print("13. Confirm Balance Due becomes ₹0: FAIL")
                
            if 'Pay Balance' not in html:
                print("14. Confirm Pay Balance disappears: OK")
            else:
                print("14. Confirm Pay Balance disappears: FAIL")
                
            if '<div class="od-timeline">' in html or 'od-timeline-step' in html:
                print("15. Confirm existing order tracking still works: OK")
            else:
                print("15. Confirm existing order tracking still works: FAIL")

run_test()
