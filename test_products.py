import urllib.request
import re

products = [
    'crochet-rose-bouquet',
    'sunflower-bouquet',
    'teddy-amigurumi',
    'daisy-bouquet',
    'tulip-bouquet',
    'mini-heart-keychain',
    'flower-bookmark'
]

for slug in products:
    try:
        url = f'http://127.0.0.1:5000/product?slug={slug}'
        req = urllib.request.urlopen(url, timeout=5)
        html = req.read().decode('utf-8', errors='ignore')
        m = re.search(r'<h1 class="product-title">(.*?)</h1>', html)
        title = m.group(1).strip() if m else None
        has_price = 'product-price' in html
        has_category = 'product-category' in html
        has_addtocart = 'add-to-cart-btn' in html
        if title:
            print(f'OK  {slug}  =>  title="{title}"  price={has_price}  cat={has_category}  cart={has_addtocart}')
        else:
            print(f'WARN {slug}: no product-title h1 found in page')
    except Exception as e:
        print(f'ERR {slug}: {e}')
