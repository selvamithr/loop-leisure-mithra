import re
import os

shop_file = r"c:\Users\sasi6\OneDrive\Desktop\loop & leisure ~mithra\app\templates\customer\shop.html"
index_file = r"c:\Users\sasi6\OneDrive\Desktop\loop & leisure ~mithra\app\templates\customer\index.html"

# Reverse shop.html
with open(shop_file, "r", encoding="utf-8") as f:
    shop_html = f.read()

shop_replacements = {
    "/static/uploads/product-image/redrose_boquet.jpeg": "https://picsum.photos/seed/rose/500/600",
    "/static/uploads/product-image/sunflower_clip.jpeg": "https://picsum.photos/seed/sunflower/500/600",
    "/static/images/mithra.jpeg": "https://picsum.photos/seed/teddy/500/600",
    "/static/uploads/product-image/mixedrose_boquet.jpeg": "https://picsum.photos/seed/daisy/500/600",
    "/static/uploads/product-image/tulip_boquet.jpeg": "https://picsum.photos/seed/tulip/500/600",
    "/static/uploads/product-image/messi_keychain.jpeg": "https://picsum.photos/seed/heart/500/600",
    "/static/uploads/product-image/flower_clip.jpeg": "https://picsum.photos/seed/bookmark/500/600"
}

for old, new in shop_replacements.items():
    shop_html = shop_html.replace(old, new)

# Remove the appended products
shop_html = re.sub(r'\n                <!-- New Product Virat Keychain -->.*?<!-- New Product Phone Charm -->.*?</style>', '</style>', shop_html, flags=re.DOTALL)
shop_html = re.sub(r'\n                <!-- New Product Virat Keychain -->.*?<div class="shop-product-price">\$10.00</div>\s*<a href="/product" class="btn btn-primary shop-product-btn">View Product</a>\s*</div>\s*</div>', '', shop_html, flags=re.DOTALL)

with open(shop_file, "w", encoding="utf-8") as f:
    f.write(shop_html)

# Reverse index.html
with open(index_file, "r", encoding="utf-8") as f:
    index_html = f.read()

index_replacements = {
    "/static/uploads/product-image/tulip_boquet.jpeg": "https://picsum.photos/seed/bouquet/600/450",
    "/static/uploads/product-image/virat_keychain.jpeg": "https://picsum.photos/seed/keychains/600/450",
    "/static/uploads/product-image/crochet_brown_pouch.jpeg": "https://picsum.photos/seed/decor/600/450",
    "/static/uploads/product-image/mixedrose_boquet.jpeg": "https://picsum.photos/seed/bouquet2/500/600",
    "/static/uploads/product-image/sunflower_clip.jpeg": "https://picsum.photos/seed/sunflower/500/600",
    "/static/images/mithra.jpeg": "https://picsum.photos/seed/lavender/500/600",
    "/static/uploads/product-image/flower_clip.jpeg": "https://picsum.photos/seed/daisy/500/600",
    "/static/uploads/product-image/crochet_hairbowclip.jpeg": "https://picsum.photos/seed/gal1/400/400",
    "/static/uploads/product-image/phone_charm.jpeg": "https://picsum.photos/seed/gal2/400/400",
    "/static/uploads/product-image/laptop_case.jpeg": "https://picsum.photos/seed/gal3/400/400",
    "/static/uploads/product-image/tulip_boquet2.jpeg": "https://picsum.photos/seed/gal4/400/400",
    "/static/uploads/product-image/scrunchies.jpeg": "https://picsum.photos/seed/gal5/400/400",
    "/static/uploads/product-image/classic_whitepouch.jpeg": "https://picsum.photos/seed/gal6/400/400",
    "/static/uploads/product-image/tulip_boquet3.jpeg": "https://picsum.photos/seed/gal7/400/400",
    "/static/uploads/product-image/brownflower_clip.jpeg": "https://picsum.photos/seed/gal8/400/400"
}

for old, new in index_replacements.items():
    index_html = index_html.replace(old, new)

with open(index_file, "w", encoding="utf-8") as f:
    f.write(index_html)

print("Reverted shop.html and index.html")
