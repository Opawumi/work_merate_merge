import os
import shutil
from PIL import Image, ImageOps

Image.MAX_IMAGE_PIXELS = None

def generate_webp_and_optimize():
    assets_dir = 'assets'
    converted = 0
    total_savings = 0
    
    for root, dirs, files in os.walk(assets_dir):
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in ('.png', '.jpg', '.jpeg'):
                orig_path = os.path.join(root, f)
                webp_path = os.path.splitext(orig_path)[0] + '.webp'
                
                try:
                    with Image.open(orig_path) as im:
                        im = ImageOps.exif_transpose(im)
                        # Save WebP with high quality
                        if im.mode in ('RGBA', 'LA', 'PA'):
                            im.save(webp_path, format='WEBP', quality=85, method=6)
                        else:
                            im.convert('RGB').save(webp_path, format='WEBP', quality=85, method=6)
                            
                        orig_sz = os.path.getsize(orig_path)
                        webp_sz = os.path.getsize(webp_path)
                        converted += 1
                        print(f"[WEBP] {webp_path}: {orig_sz/1024:.1f} KB -> {webp_sz/1024:.1f} KB ({((orig_sz-webp_sz)/orig_sz)*100:.1f}% saved)")
                except Exception as e:
                    print(f"Error converting {orig_path} to webp: {e}")

    print(f"\nCreated {converted} optimized WebP images.")

if __name__ == '__main__':
    generate_webp_and_optimize()
