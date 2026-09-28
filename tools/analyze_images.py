import os
import sys
from PIL import Image

def analyze_assets():
    results = []
    for root, dirs, files in os.walk('assets'):
        for f in files:
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                path = os.path.join(root, f)
                sz = os.path.getsize(path)
                try:
                    with Image.open(path) as im:
                        results.append({
                            'path': path,
                            'size': sz,
                            'width': im.width,
                            'height': im.height,
                            'format': im.format,
                            'mode': im.mode
                        })
                except Exception as e:
                    print(f"Error opening {path}: {e}")
    
    results.sort(key=lambda x: x['size'], reverse=True)
    print(f"Total images found: {len(results)}")
    total_size = sum(r['size'] for r in results)
    print(f"Total assets size: {total_size / 1024 / 1024:.2f} MB")
    print("\nTop 20 heaviest images:")
    for r in results[:20]:
        print(f"  {r['size']/1024/1024:6.2f} MB ({r['size']/1024:7.1f} KB) | {r['width']:5d}x{r['height']:<5d} | {r['mode']:4s} | {r['path']}")

if __name__ == '__main__':
    analyze_assets()
