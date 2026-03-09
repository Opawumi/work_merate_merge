import glob
import re
import os

html_files = glob.glob('*.html')
for f in html_files:
    try:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
    except Exception as e:
        print(f"Error reading {f}: {e}")
        continue
    
    # Find links with href="#" or href=""
    # This regex looks for <a> tags where the href is # or empty
    # And tries to capture the text inside
    matches = re.findall(r'<a[^>]+href=["\']#?["\'][^>]*>(.*?)</a>', content, re.IGNORECASE | re.DOTALL)
    for m in matches:
        # Strip internal tags to get plain text
        text = re.sub('<[^<]+?>', '', m).strip()
        if 'Marketing Automation' in text:
            print(f"{f}: Marketing Automation link is broken (#)")
        if 'Login' in text:
            print(f"{f}: Login link is broken (#)")
        if any(kw in text for kw in ['Try it Free', 'Sign up', 'Sign Up']):
            print(f"{f}: Signup link is broken (#)")
