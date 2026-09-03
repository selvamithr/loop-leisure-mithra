import os
import urllib.request

dest_dir = r"c:\Users\sasi6\OneDrive\Desktop\loop & leisure ~mithra\app\static\uploads\product-image"

files = {
    "virat_keychain.jpeg": "Virat+Keychain",
    "crochet_hair_accessories.jpeg": "Hair+Accessories",
    "crochet_brown_pouch.jpeg": "Brown+Pouch", 
    "messi_keychain.jpeg": "Messi+Keychain",
    "classic_whitepouch.jpeg": "White+Pouch",
    "redrose_boquet.jpeg": "Red+Rose+Bouquet", 
    "phone_charm.jpeg": "Phone+Charm",
    "phone_charm2.jpeg": "Phone+Charm+2",
    "scrunchies.jpeg": "Scrunchies",
    "sunflower_clip.jpeg": "Sunflower+Clip", 
    "crochet_hairbowclip.jpeg": "Hairbow+Clip",
    "flower_clip.jpeg": "Flower+Clip",
    "brownflower_clip.jpeg": "Brown+Flower+Clip", 
    "laptop_case.jpeg": "Laptop+Case",
    "heart_bouquet.jpeg": "Heart+Bouquet",
    "tulip_boquet.jpeg": "Tulip+Bouquet", 
    "tulip_boquet2.jpeg": "Tulip+Bouquet+2",
    "tulip_boquet3.jpeg": "Tulip+Bouquet+3",
    "mixedrose_boquet.jpeg": "Mixed+Rose+Bouquet",
    "WhatsApp Image 2026-08-15 at 9.25.06 A...jpeg": "WhatsApp+Image"
}

for filename, text in files.items():
    url = f"https://placehold.co/500x600/png?text={text}"
    try:
        urllib.request.urlretrieve(url, os.path.join(dest_dir, filename))
        print(f"Downloaded {filename}")
    except Exception as e:
        print(f"Failed to download {filename}: {e}")

print("Fixed images.")
