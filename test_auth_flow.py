import requests
import json

def test_auth_flow():
    s = requests.Session()
    base_url = "http://127.0.0.1:5000"
    
    print("1. Testing unauthenticated Add to Cart (AJAX)")
    r = s.post(f"{base_url}/cart/add", json={"product_id": "crochet-rose-bouquet", "quantity": 1})
    assert r.status_code == 401
    data = r.json()
    assert data['success'] == False
    assert '/login' in data['redirect']
    print("AJAX Add to Cart returned correct redirect JSON.")
    
    # We must check if the flash message was queued. 
    # Fetching the login page (which we are redirected to) should show it.
    r_login = s.get(data['redirect'])
    assert "Please log in or create an account to add items to your cart." in r_login.text
    print("Flash message for Cart correctly displayed on Login page.")

    # Clear session by creating a new one (though not strictly necessary as login flashed message clears it)
    s = requests.Session()
    
    print("2. Testing unauthenticated Proceed to Checkout")
    r = s.get(f"{base_url}/checkout", allow_redirects=False)
    assert r.status_code == 302
    assert '/login' in r.headers['Location']
    
    # Follow redirect to login page
    r_login2 = s.get(base_url + r.headers['Location'])
    assert "Please log in to continue with your order." in r_login2.text
    print("Flash message for Checkout correctly displayed on Login page.")
    
    print("All auth flow tests passed successfully!")

if __name__ == "__main__":
    test_auth_flow()
