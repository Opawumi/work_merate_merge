import os
from PIL import Image, ImageOps

Image.MAX_IMAGE_PIXELS = None  # Allow processing large images

def optimize_image(input_path, max_dim=1920, quality=85):
    orig_size = os.path.getsize(input_path)
    
    with Image.open(input_path) as im:
        # Check orientation
        im = ImageOps.exif_transpose(im)
        w, h = im.size
        
        # Resize if overly large
        if max(w, h) > max_dim:
            scale = max_dim / max(w, h)
            new_w = int(w * scale)
            new_h = int(h * scale)
            im = im.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        # Check transparency
        has_alpha = False
        if im.mode in ('RGBA', 'LA', 'PA'):
            # Check if any pixels are actually translucent/transparent
            alpha = im.getchannel('A')
            min_a, max_a = alpha.getextrema()
            if min_a < 255:
                has_alpha = True
            else:
                im = im.convert('RGB')
        elif im.mode != 'RGB':
            im = im.convert('RGB')
            
        temp_path = input_path + '.tmp'
        
        if input_path.lower().endswith('.png'):
            if has_alpha:
                im.save(temp_path, format='PNG', optimize=True, compress_level=9)
            else:
                # Try optimized RGB PNG
                im.save(temp_path, format='PNG', optimize=True, compress_level=9)
        elif input_path.lower().endswith(('.jpg', '.jpeg')):
            im.save(temp_path, format='JPEG', quality=quality, optimize=True)
        elif input_path.lower().endswith('.webp'):
            im.save(temp_path, format='WEBP', quality=quality, method=6)
            
        new_size = os.path.getsize(temp_path)
        
        print(f"{input_path}:")
        print(f"  Orig: {w}x{h}, {orig_size/1024:.1f} KB ({orig_size/1024/1024:.2f} MB)")
        print(f"  New : {im.size[0]}x{im.size[1]}, {new_size/1024:.1f} KB ({new_size/1024/1024:.2f} MB) -> Saved {((orig_size-new_size)/orig_size)*100:.1f}%")
        
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == '__main__':
    test_files = [
        'assets/about-us-hero.png',
        'assets/hero.png',
        'assets/login_image.png',
        'assets/signup_image.png',
        'assets/hero image 2.png',
        'assets/imggggg-mobile (2).png',
        'assets/integration-visual.png',
        'assets/tax-management/tax-mgt-hero-bg.png',
        'assets/Hero-mob.png'
    ]
    for tf in test_files:
        if os.path.exists(tf):
            optimize_image(tf)
