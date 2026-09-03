import sys, os

# Add project root to sys.path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

from app import create_app

app = create_app('development')

endpoints = ['/about', '/faq', '/contact', '/custom-order']
with app.test_client() as client:
    all_ok = True
    for ep in endpoints:
        resp = client.get(ep)
        print(f'{ep}: {resp.status_code}')
        if resp.status_code != 200:
            all_ok = False
    sys.exit(0 if all_ok else 1)
