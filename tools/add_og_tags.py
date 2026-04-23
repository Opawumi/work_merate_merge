import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_FILES = list(ROOT.glob('*.html'))
DEFAULT_IMAGE = 'https://workmeraterp.com.ng/assets/about-us-hero.png'
TWITTER_SITE = '@WorkMerate'

meta_template = '''    <!-- Open Graph / Twitter Card -->
    <meta property="og:site_name" content="WorkMerate" />
    <meta property="og:title" content="{title}" />
    <meta property="og:description" content="{description}" />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="{url}" />
    <meta property="og:image" content="{image}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="{twitter}" />
    <meta name="twitter:creator" content="{twitter}" />
    <meta name="twitter:title" content="{title}" />
    <meta name="twitter:description" content="{description}" />
    <meta name="twitter:image" content="{image}" />
'''

for f in HTML_FILES:
    s = f.read_text(encoding='utf-8')
    # skip if OG already present
    if 'property="og:title"' in s or 'name="twitter:card"' in s:
        print(f.name, 'already has OG/tags, skipping')
        continue
    # find meta description
    m = re.search(r"<meta\s+name=\"description\"\s+content=\"([\s\S]*?)\"\s*/?>", s)
    if m:
        description = m.group(1).strip()
    else:
        description = ''
    # find title
    t = re.search(r"<title>([\s\S]*?)</title>", s)
    title = t.group(1).strip() if t else f.stem
    # find canonical
    c = re.search(r"<link\s+rel=\"canonical\"\s+href=\"([\s\S]*?)\"\s*/?>", s)
    if c:
        url = c.group(1).strip()
    else:
        url = f'https://workmeraterp.com.ng/{f.name}'
    block = meta_template.format(title=title.replace('"','&quot;'), description=description.replace('"','&quot;'), url=url, image=DEFAULT_IMAGE, twitter=TWITTER_SITE)
    # insert after description meta if exists, else after <head>
    if m:
        insert_pos = m.end()
        new_s = s[:insert_pos] + '\n' + block + s[insert_pos:]
    else:
        # insert after <head>
        new_s = s.replace('<head>', '<head>\n' + block, 1)
    f.write_text(new_s, encoding='utf-8')
    print('Updated', f.name)
print('Done')
