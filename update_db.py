import sqlite3
import os

new_products = [
    ('Virat Keychain', 'virat-keychain', 15.0, 'Keychains', 'virat_keychain.jpeg'),
    ('Messi Keychain', 'messi-keychain', 15.0, 'Keychains', 'messi_keychain.jpeg'),
    ('Phone Charm', 'phone-charm', 10.0, 'Accessories', 'phone_charm.jpeg'),
    ('Phone Charm 2', 'phone-charm-2', 10.0, 'Accessories', 'phone_charm2.jpeg'),
    ('Crochet Hair Accessories', 'crochet-hair-accessories', 20.0, 'Accessories', 'crochet_hair_accessories.jpeg'),
    ('Crochet Brown Pouch', 'crochet-brown-pouch', 25.0, 'Accessories', 'crochet_brown_pouch.jpeg'),
    ('Classic White Pouch', 'classic-white-pouch', 25.0, 'Accessories', 'classic_whitepouch.jpeg'),
    ('Scrunchies', 'scrunchies', 8.0, 'Accessories', 'scrunchies.jpeg'),
    ('Crochet Hairbowclip', 'crochet-hairbowclip', 12.0, 'Accessories', 'crochet_hairbowclip.jpeg'),
    ('Brownflower Clip', 'brownflower-clip', 12.0, 'Accessories', 'brownflower_clip.jpeg'),
    ('Laptop Case', 'laptop-case', 45.0, 'Accessories', 'laptop_case.jpeg'),
    ('Tulip Bouquet 3', 'tulip-bouquet-3', 42.0, 'Bouquets', 'tulip_boquet3.jpeg'),
    ('Special Custom Item', 'special-custom-item', 30.0, 'Others', 'WhatsApp Image 2026-08-15 at 9.25.06 A...jpeg')
]

conn = sqlite3.connect('instance/database.db')
cursor = conn.cursor()

# Get max id
cursor.execute('SELECT MAX(id) FROM products')
max_id = cursor.fetchone()[0] or 0

for p in new_products:
    max_id += 1
    cursor.execute('''INSERT INTO products 
        (id, name, slug, description, category, price, advance_percentage, stock_status, is_featured, created_at) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)''',
        (max_id, p[0], p[1], 'A beautiful handmade product.', p[3], p[2], 0, 'in_stock', 0))
    cursor.execute('''INSERT INTO product_images (product_id, image_path, display_order) VALUES (?, ?, ?)''',
        (max_id, f'/static/uploads/product-image/{p[4]}', 1))

# Update existing images in DB just in case
cursor.execute("UPDATE product_images SET image_path = '/static/uploads/product-image/redrose_boquet.jpeg' WHERE product_id = 1")
cursor.execute("UPDATE product_images SET image_path = '/static/uploads/product-image/sunflower_clip.jpeg' WHERE product_id = 2")
# June Keychain was ID 3, already removed from HTML, we should remove from DB
cursor.execute("DELETE FROM products WHERE id = 3")
cursor.execute("DELETE FROM product_images WHERE product_id = 3")

cursor.execute("UPDATE product_images SET image_path = '/static/images/ChatGPT Image Jul 2, 2026, 10_50_11 PM.png' WHERE product_id = 4")
cursor.execute("UPDATE product_images SET image_path = '/static/uploads/product-image/mixedrose_boquet.jpeg' WHERE product_id = 5")
cursor.execute("UPDATE product_images SET image_path = '/static/uploads/product-image/tulip_boquet.jpeg' WHERE product_id = 6")
cursor.execute("UPDATE product_images SET image_path = '/static/uploads/product-image/messi_keychain.jpeg' WHERE product_id = 7")
cursor.execute("UPDATE product_images SET image_path = '/static/uploads/product-image/flower_clip.jpeg' WHERE product_id = 8")

conn.commit()
conn.close()

print("Database updated!")
