import os
import re
import io
import base64
import shutil
from PIL import Image, ImageOps

Image.MAX_IMAGE_PIXELS = None  # Allow large image processing

def optimize_svg_embedded_images(svg_path):
    orig_sz = os.path.getsize(svg_path)
    try:
        with open(svg_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        def repl(match):
            prefix = match.group(1) # e.g. xlink:href="data:image/png;base64,
            b64_data = match.group(2)
            suffix = match.group(3)
            try:
                raw = base64.b64decode(b64_data)
                im = Image.open(io.BytesIO(raw))
                w, h = im.size
                # If embedded image is larger than 512 in any dim, scale down
                if max(w, h) > 512:
                    im.thumbnail((512, 512), Image.Resampling.LANCZOS)
                buf = io.BytesIO()
                if im.mode == 'RGBA':
                    im.save(buf, format='PNG', optimize=True, compress_level=9)
                else:
                    im.convert('RGB').save(buf, format='JPEG', quality=85, optimize=True)
                new_b64 = base64.b64encode(buf.getvalue()).decode('ascii')
                return f'{prefix}{new_b64}{suffix}'
            except Exception as e:
                print(f"Error processing embedded image in SVG {svg_path}: {e}")
                return match.group(0)

        # Match base64 data images inside SVG
        pattern = r'(xlink:href=["\']data:image/[^;]+;base64,)([^"\']+)(["\'])'
        new_content = re.sub(pattern, repl, content)
        
        pattern_src = r'(src=["\']data:image/[^;]+;base64,)([^"\']+)(["\'])'
        new_content = re.sub(pattern_src, repl, new_content)
        
        if len(new_content) < len(content):
            with open(svg_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            new_sz = os.path.getsize(svg_path)
            print(f"[SVG] {svg_path}: {orig_sz/1024:.1f} KB -> {new_sz/1024:.1f} KB ({((orig_sz-new_sz)/orig_sz)*100:.1f}% saved)")
    except Exception as e:
        print(f"Failed to process SVG {svg_path}: {e}")

def optimize_raster_image(path):
    orig_sz = os.path.getsize(path)
    if orig_sz < 5 * 1024:  # Skip tiny icons < 5KB
        return
        
    try:
        with Image.open(path) as im:
            im = ImageOps.exif_transpose(im)
            w, h = im.size
            orig_mode = im.mode
            
            # Determine maximum dimension
            # Hero/visual backgrounds: max 1920px
            # Mobile hero/graphics: max 1080px
            # Standard cards/illustrations: max 1200px
            lower_name = os.path.basename(path).lower()
            if 'mob' in lower_name:
                max_dim = 1080
            elif any(k in lower_name for k in ['hero', 'banner', 'bg', 'visual', 'container', 'problem']):
                max_dim = 1920
            else:
                max_dim = 1200
                
            needs_resize = max(w, h) > max_dim
            if needs_resize:
                scale = max_dim / max(w, h)
                new_w = max(1, int(w * scale))
                new_h = max(1, int(h * scale))
                im = im.resize((new_w, new_h), Image.Resampling.LANCZOS)
                
            # Check transparency for RGBA
            has_real_alpha = False
            if im.mode in ('RGBA', 'LA', 'PA'):
                alpha = im.getchannel('A')
                extrema = alpha.getextrema()
                if extrema[0] < 255:  # Has non-opaque pixels
                    has_real_alpha = True
                else:
                    im = im.convert('RGB')
            elif im.mode not in ('RGB', 'L'):
                im = im.convert('RGB')
                
            temp_path = path + '.tmp_opt'
            fmt = im.format or ('PNG' if path.lower().endswith('.png') else 'JPEG' if path.lower().endswith(('.jpg', '.jpeg')) else 'WEBP')
            
            if path.lower().endswith('.png'):
                im.save(temp_path, format='PNG', optimize=True, compress_level=9)
            elif path.lower().endswith(('.jpg', '.jpeg')):
                im.save(temp_path, format='JPEG', quality=85, optimize=True)
            elif path.lower().endswith('.webp'):
                im.save(temp_path, format='WEBP', quality=85, method=6)
                
            new_sz = os.path.getsize(temp_path)
            
            # If temp file is actually smaller, replace original
            if new_sz < orig_sz:
                shutil.move(temp_path, path)
                saved_pct = ((orig_sz - new_sz) / orig_sz) * 100
                print(f"[OK] {path} ({w}x{h} -> {im.size[0]}x{im.size[1]}): {orig_sz/1024:.1f} KB -> {new_sz/1024:.1f} KB ({saved_pct:.1f}% saved)")
            else:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                print(f"[SKIP] {path}: already optimal ({orig_sz/1024:.1f} KB)")
    except Exception as e:
        print(f"[ERROR] Failed {path}: {e}")

def main():
    print("Starting comprehensive image asset optimization...")
    assets_dir = 'assets'
    for root, dirs, files in os.walk(assets_dir):
        for f in files:
            p = os.path.join(root, f)
            ext = f.lower()
            if ext.endswith('.svg'):
                optimize_svg_embedded_images(p)
            elif ext.endswith(('.png', '.jpg', '.jpeg', '.webp')):
                optimize_raster_image(p)
                
    print("\nOptimization completed.")

if __name__ == '__main__':
    main()
