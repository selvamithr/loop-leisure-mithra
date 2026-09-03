import os
import shutil

src = r"c:\Users\sasi6\OneDrive\Desktop\loop & leisure ~mithra\app\static\images\mithra.jpeg"
dest_dir = r"c:\Users\sasi6\OneDrive\Desktop\loop & leisure ~mithra\app\static\uploads\product-image"

if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

files = [
    "virat_keychain.jpeg", "crochet_hair_accessories.jpeg", "crochet_brown_pouch.jpeg", 
    "messi_keychain.jpeg", "classic_whitepouch.jpeg", "redrose_boquet.jpeg", 
    "phone_charm.jpeg", "phone_charm2.jpeg", "scrunchies.jpeg", "sunflower_clip.jpeg", 
    "crochet_hairbowclip.jpeg", "flower_clip.jpeg", "brownflower_clip.jpeg", 
    "laptop_case.jpeg", "heart_bouquet.jpeg", "tulip_boquet.jpeg", 
    "tulip_boquet2.jpeg", "tulip_boquet3.jpeg", "mixedrose_boquet.jpeg",
    "WhatsApp Image 2026-08-15 at 9.25.06 A...jpeg"
]

for f in files:
    shutil.copy(src, os.path.join(dest_dir, f))
print("Copied fake images.")
