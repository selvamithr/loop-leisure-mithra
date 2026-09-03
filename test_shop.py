import urllib.request

req = urllib.request.urlopen('http://127.0.0.1:5000/shop', timeout=5)
html = req.read().decode('utf-8', errors='ignore')

# Check all slugs present
slugs = ['crochet-rose-bouquet', 'sunflower-bouquet', 'teddy-amigurumi',
         'daisy-bouquet', 'tulip-bouquet', 'mini-heart-keychain', 'flower-bookmark']
for s in slugs:
    found = s in html
    print(f'  slug={s}: {"FOUND" if found else "MISSING"}')

if 'June Keychain' in html or 'june-keychain' in html:
    print('FAIL: June Keychain still present!')
else:
    print('OK: June Keychain is completely absent.')
