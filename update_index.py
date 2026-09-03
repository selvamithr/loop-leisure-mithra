import re

index_file = r"c:\Users\sasi6\OneDrive\Desktop\loop & leisure ~mithra\app\templates\customer\index.html"

with open(index_file, "r", encoding="utf-8") as f:
    html = f.read()

replacements = {
    "https://picsum.photos/seed/bouquet/600/450": "/static/uploads/product-image/tulip_boquet.jpeg",
    "https://picsum.photos/seed/keychains/600/450": "/static/uploads/product-image/virat_keychain.jpeg",
    "https://picsum.photos/seed/decor/600/450": "/static/uploads/product-image/crochet_brown_pouch.jpeg",
    "https://picsum.photos/seed/bouquet2/500/600": "/static/uploads/product-image/mixedrose_boquet.jpeg",
    "https://picsum.photos/seed/sunflower/500/600": "/static/uploads/product-image/sunflower_clip.jpeg",
    "https://picsum.photos/seed/lavender/500/600": "/static/images/mithra.jpeg",
    "https://picsum.photos/seed/daisy/500/600": "/static/uploads/product-image/flower_clip.jpeg",
    "https://picsum.photos/seed/gal1/400/400": "/static/uploads/product-image/crochet_hairbowclip.jpeg",
    "https://picsum.photos/seed/gal2/400/400": "/static/uploads/product-image/phone_charm.jpeg",
    "https://picsum.photos/seed/gal3/400/400": "/static/uploads/product-image/laptop_case.jpeg",
    "https://picsum.photos/seed/gal4/400/400": "/static/uploads/product-image/tulip_boquet2.jpeg",
    "https://picsum.photos/seed/gal5/400/400": "/static/uploads/product-image/scrunchies.jpeg",
    "https://picsum.photos/seed/gal6/400/400": "/static/uploads/product-image/classic_whitepouch.jpeg",
    "https://picsum.photos/seed/gal7/400/400": "/static/uploads/product-image/tulip_boquet3.jpeg",
    "https://picsum.photos/seed/gal8/400/400": "/static/uploads/product-image/brownflower_clip.jpeg"
}

for old, new in replacements.items():
    html = html.replace(old, new)

with open(index_file, "w", encoding="utf-8") as f:
    f.write(html)

print("Updated index.html")
