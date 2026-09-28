import os
from PIL import Image

def test_formats(path):
    orig_sz = os.path.getsize(path)
    im = Image.open(path)
    if im.mode == 'RGBA':
        # Check if alpha is used
        extrema = im.getextrema()
        if extrema[3][0] == 255:
            im = im.convert('RGB')
    elif im.mode != 'RGB':
        im = im.convert('RGB')
        
    print(f"\nTesting {path} (Original: {orig_sz/1024:.1f} KB):")
    
    # 1. WebP quality 85
    im.save('tmp_test.webp', 'WEBP', quality=85, method=6)
    print(f"  WebP (q=85): {os.path.getsize('tmp_test.webp')/1024:.1f} KB")
    
    # 2. WebP quality 80
    im.save('tmp_test.webp', 'WEBP', quality=80, method=6)
    print(f"  WebP (q=80): {os.path.getsize('tmp_test.webp')/1024:.1f} KB")
    
    # 3. JPEG quality 85
    if im.mode == 'RGB':
        im.save('tmp_test.jpg', 'JPEG', quality=85, optimize=True)
        print(f"  JPEG (q=85): {os.path.getsize('tmp_test.jpg')/1024:.1f} KB")
        
    # 4. Quantized PNG (256 colors)
    q_im = im.quantize(colors=256, method=Image.Quantize.MEDIANCUT)
    q_im.save('tmp_test.png', 'PNG', optimize=True)
    print(f"  Quantized PNG (256c): {os.path.getsize('tmp_test.png')/1024:.1f} KB")

if __name__ == '__main__':
    for p in ['assets/about-us-hero.png', 'assets/hero.png', 'assets/login_image.png', 'assets/signup_image.png']:
        test_formats(p)
    if os.path.exists('tmp_test.webp'): os.remove('tmp_test.webp')
    if os.path.exists('tmp_test.jpg'): os.remove('tmp_test.jpg')
    if os.path.exists('tmp_test.png'): os.remove('tmp_test.png')
