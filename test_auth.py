import requests

def run_auth_tests():
    s = requests.Session()
    base_url = "http://127.0.0.1:5000"
    
    print("1. Testing unauthenticated access to /cart (should redirect to /login)")
    r = s.get(f"{base_url}/cart", allow_redirects=False)
    assert r.status_code == 302
    assert '/login' in r.headers['Location']
    print("Passed.")
    
    print("2. Testing Registration")
    reg_data = {
        'full_name': 'Test User',
        'email': 'testuser@example.com',
        'phone': '9999999999',
        'password': 'password123',
        'confirm_password': 'password123'
    }
    r = s.post(f"{base_url}/register", data=reg_data, allow_redirects=False)
    assert r.status_code == 302
    assert '/' in r.headers['Location']
    print("Passed.")
    
    print("3. Testing Cart access after login (should be 200)")
    r = s.get(f"{base_url}/cart")
    assert r.status_code == 200
    print("Passed.")
    
    print("4. Testing Logout")
    r = s.get(f"{base_url}/logout", allow_redirects=False)
    assert r.status_code == 302
    print("Passed.")
    
    print("5. Testing unauthenticated Cart API (should redirect to /login due to @login_required)")
    r = s.post(f"{base_url}/cart/add", json={"product_id": "crochet-rose-bouquet", "quantity": 1}, allow_redirects=False)
    assert r.status_code == 302
    print("Passed.")
    
    print("6. Testing Login")
    login_data = {
        'email': 'testuser@example.com',
        'password': 'password123'
    }
    r = s.post(f"{base_url}/login", data=login_data, allow_redirects=False)
    assert r.status_code == 302
    print("Passed.")
    
    print("7. Testing Duplicate Email Registration")
    s.get(f"{base_url}/logout") # Logout first!
    r = s.post(f"{base_url}/register", data=reg_data, allow_redirects=False)
    assert r.status_code == 302
    assert '/login' in r.headers['Location']
    print("Passed.")
    
    print("8. Testing Cart additions with authenticated user")
    r = s.post(f"{base_url}/cart/add", json={"product_id": "crochet-rose-bouquet", "quantity": 1})
    assert r.status_code == 200
    assert r.json()['success'] == True
    print("Passed.")

    print("All auth tests passed!")

if __name__ == "__main__":
    run_auth_tests()
