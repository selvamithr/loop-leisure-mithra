import requests

def run_tests():
    s = requests.Session()
    base_url = "http://127.0.0.1:5000"
    
    print("1. Testing Cart Count (should be 0)")
    r = s.get(f"{base_url}/cart/count")
    print(r.json())
    assert r.json()['cart_count'] == 0
    
    print("2. Testing Add to Cart")
    r = s.post(f"{base_url}/cart/add", json={"product_id": "crochet-rose-bouquet", "quantity": 1})
    print(r.json())
    assert r.json()['success'] == True
    assert r.json()['cart_count'] == 1
    
    print("3. Testing Cart Count (should be 1)")
    r = s.get(f"{base_url}/cart/count")
    print(r.json())
    assert r.json()['cart_count'] == 1
    
    print("4. Testing Increase Quantity (add 2 more)")
    r = s.post(f"{base_url}/cart/add", json={"product_id": "crochet-rose-bouquet", "quantity": 2})
    print(r.json())
    assert r.json()['cart_count'] == 3
    
    print("5. Testing Update Quantity (set to 5)")
    r = s.post(f"{base_url}/cart/update", json={"product_id": "crochet-rose-bouquet", "quantity": 5})
    print(r.json())
    assert r.json()['cart_count'] == 5
    
    print("6. Testing Decrease Quantity (set to 2)")
    r = s.post(f"{base_url}/cart/update", json={"product_id": "crochet-rose-bouquet", "quantity": 2})
    print(r.json())
    assert r.json()['cart_count'] == 2
    
    print("7. Testing Remove Item")
    r = s.post(f"{base_url}/cart/remove", json={"product_id": "crochet-rose-bouquet"})
    print(r.json())
    assert r.json()['cart_count'] == 0
    
    print("8. Testing Cart UI page")
    r = s.get(f"{base_url}/cart")
    assert r.status_code == 200
    if "Your cart is empty" in r.text:
        print("Empty cart UI is rendering correctly.")
    else:
        print("Warning: Empty cart UI not found.")
        
    print("All tests passed!")

if __name__ == "__main__":
    run_tests()
