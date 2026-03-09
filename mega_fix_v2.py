import glob
import re
import os

def mega_fix():
    # 1. Read the master navbar from index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        master_content = f.read()
    
    # Extract nav block
    nav_match = re.search(r'(<nav.*?</nav>)', master_content, re.IGNORECASE | re.DOTALL)
    if not nav_match:
        print("Could not find navbar in index.html")
        return
    
    master_nav_raw = nav_match.group(1)
    
    html_files = [f for f in glob.glob('*.html') if f != 'index.html' and f != 'check_links.py' and f != 'mega_fix.py' and f != 'mega_fix_v2.py']
    
    for filename in html_files:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 2. Extract specific active flag if useful, but we'll try to synthesize it.
            # Start with a clean master_nav for this file.
            this_nav = master_nav_raw
            
            # Highlight this page in top-level nav if applicable.
            # Top-level links like <a href="filename" class="nav-link">
            # We need to find if filename exists in the nav links.
            # e.g. for pricing.html, we want <a href="pricing.html" class="nav-link"> -> <a href="pricing.html" class="nav-link active">
            
            # Special case for modules pages (they should all highlight Modules dropdown?)
            modules_pages = ['hr.html', 'financial-management.html', 'marketing-automation.html', 'tax-management.html', 
                             'project-management.html', 'productivity-management.html', 'sc-management.html', 'custom-modules.html']
            if filename in modules_pages:
                this_nav = this_nav.replace('href="custom-modules.html" class="nav-link"', 'href="custom-modules.html" class="nav-link active"')
            elif filename == 'agentic-ai.html':
                this_nav = this_nav.replace('href="agentic-ai.html" class="nav-link"', 'href="agentic-ai.html" class="nav-link active"')
            elif filename == 'services.html':
                 this_nav = this_nav.replace('href="services.html" class="nav-link"', 'href="services.html" class="nav-link active"')
            elif filename == 'pricing.html':
                 this_nav = this_nav.replace('href="pricing.html" class="nav-link"', 'href="pricing.html" class="nav-link active"')
            elif filename == 'about.html':
                 this_nav = this_nav.replace('href="about.html" class="nav-link"', 'href="about.html" class="nav-link active"')
            elif filename == 'learning.html':
                 this_nav = this_nav.replace('href="learning.html" class="nav-link"', 'href="learning.html" class="nav-link active"')

            # Re-insert the navbar
            new_content = re.sub(r'(<!-- Navbar -->\s*)?<nav.*?</nav>', '<!-- Navbar -->\n  ' + this_nav, content, flags=re.IGNORECASE | re.DOTALL)
            
            # 3. Fix broken links globally (footer, etc.)
            # Marketing Automation
            # We need to be careful not to replace text in content, only in <a> tags.
            def fix_link(match):
                attr, text, text2 = match.groups()
                # If href is #, replace it
                new_attr = re.sub(r'href=["\']#["\']', 'href="marketing-automation.html"', attr)
                # If href is missing, add it
                if 'href' not in new_attr:
                     new_attr += ' href="marketing-automation.html"'
                return f'<a{new_attr}>{text}Marketing Automation{text2}</a>'

            new_content = re.sub(r'<a([^>]+)>(.*?)Marketing Automation(.*?)</a>', fix_link, new_content, flags=re.IGNORECASE | re.DOTALL)
            
            # Login
            def fix_login(match):
                attr, text, text2 = match.groups()
                if 'href="#"' in attr or 'href=\'#\'' in attr:
                    new_attr = attr.replace('href="#"', 'href="login.html"').replace("href='#'", 'href="login.html"')
                    return f'<a{new_attr}>{text}Login{text2}</a>'
                return match.group(0)

            new_content = re.sub(r'<a([^>]+)>(.*?)Login(.*?)</a>', fix_login, new_content, flags=re.IGNORECASE | re.DOTALL)

            # Signup / Try it Free
            def fix_signup(match):
                attr, text, text2 = match.groups()
                if 'href="#"' in attr or 'href=\'#\'' in attr:
                    new_attr = attr.replace('href="#"', 'href="signup.html"').replace("href='#'", 'href="signup.html"')
                    return f'<a{new_attr}>{text}{match.group(2)}{text2}</a>'
                return match.group(0)

            for kw in ['Sign up', 'Sign Up', 'Try it Free']:
                new_content = re.sub(r'<a([^>]+)>(.*?)' + kw + r'(.*?)</a>', fix_signup, new_content, flags=re.IGNORECASE | re.DOTALL)

            with open(filename, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {filename}")
            
        except Exception as e:
            print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    mega_fix()
