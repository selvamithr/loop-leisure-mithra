import re

shop_file = r"c:\Users\sasi6\OneDrive\Desktop\loop & leisure ~mithra\app\templates\customer\shop.html"

with open(shop_file, "r", encoding="utf-8") as f:
    html = f.read()

replacements = {
    "https://picsum.photos/seed/rose/500/600": "/static/uploads/product-image/redrose_boquet.jpeg",
    "https://picsum.photos/seed/sunflower/500/600": "/static/uploads/product-image/sunflower_clip.jpeg",
    "https://picsum.photos/seed/teddy/500/600": "/static/images/mithra.jpeg",
    "https://picsum.photos/seed/daisy/500/600": "/static/uploads/product-image/mixedrose_boquet.jpeg",
    "https://picsum.photos/seed/tulip/500/600": "/static/uploads/product-image/tulip_boquet.jpeg",
    "https://picsum.photos/seed/heart/500/600": "/static/uploads/product-image/messi_keychain.jpeg",
    "https://picsum.photos/seed/bookmark/500/600": "/static/uploads/product-image/flower_clip.jpeg"
}

for old, new in replacements.items():
    html = html.replace(old, new)

# Add new products
new_products_html = """
                <!-- New Product Virat Keychain -->
                <div class="shop-product-card" data-category="keychains">
                    <div class="shop-product-img-wrap">
                        <img src="/static/uploads/product-image/virat_keychain.jpeg" alt="Virat Keychain" class="shop-product-img" loading="lazy">
                    </div>
                    <div class="shop-product-info">
                        <div class="shop-product-rating" aria-label="5 out of 5 stars">★★★★★</div>
                        <h3 class="shop-product-title">Virat Keychain</h3>
                        <div class="shop-product-category">Keychains</div>
                        <div class="shop-product-price">$15.00</div>
                        <a href="/product" class="btn btn-primary shop-product-btn">View Product</a>
                    </div>
                </div>

                <!-- New Product Crochet Hair Accessories -->
                <div class="shop-product-card" data-category="accessories">
                    <div class="shop-product-img-wrap">
                        <img src="/static/uploads/product-image/crochet_hair_accessories.jpeg" alt="Crochet Hair Accessories" class="shop-product-img" loading="lazy">
                    </div>
                    <div class="shop-product-info">
                        <div class="shop-product-rating" aria-label="5 out of 5 stars">★★★★★</div>
                        <h3 class="shop-product-title">Crochet Hair Accessories</h3>
                        <div class="shop-product-category">Accessories</div>
                        <div class="shop-product-price">$20.00</div>
                        <a href="/product" class="btn btn-primary shop-product-btn">View Product</a>
                    </div>
                </div>

                <!-- New Product Phone Charm -->
                <div class="shop-product-card" data-category="accessories">
                    <div class="shop-product-img-wrap">
                        <img src="/static/uploads/product-image/phone_charm.jpeg" alt="Phone Charm" class="shop-product-img" loading="lazy">
                    </div>
                    <div class="shop-product-info">
                        <div class="shop-product-rating" aria-label="5 out of 5 stars">★★★★★</div>
                        <h3 class="shop-product-title">Phone Charm</h3>
                        <div class="shop-product-category">Accessories</div>
                        <div class="shop-product-price">$10.00</div>
                        <a href="/product" class="btn btn-primary shop-product-btn">View Product</a>
                    </div>
                </div>
"""

html = html.replace('</div>\n        </div>\n    </section>', new_products_html + '\n            </div>\n        </div>\n    </section>')

with open(shop_file, "w", encoding="utf-8") as f:
    f.write(html)

print("Updated shop.html")
