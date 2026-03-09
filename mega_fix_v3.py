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
    
    html_files = [f for f in glob.glob('*.html') if f != 'index.html' and f != 'check_links.py' and f != 'mega_fix.py' and f != 'mega_fix_v2.py' and f != 'mega_fix_v3.py']
    
    for filename in html_files:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Start with a clean master_nav for this file.
            this_nav = master_nav_raw
            
            # Highlight this page in top-level nav if applicable.
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
            
            # Fix broken links globally (footer, etc.)
            # We look for <a href="#" ...> or <a ... href="#" ...>
            
            def patch_links(text_content):
                # Fix Marketing Automation
                text_content = re.sub(r'<a([^>]+href=["\']#["\'][^>]*)>(.*?)Marketing Automation(.*?)</a>', 
                                     r'<a\1 href="marketing-automation.html">\2Marketing Automation\3</a>', text_content, flags=re.IGNORECASE | re.DOTALL)
                # Alternative: href is just #, no other attributes
                text_content = re.sub(r'<a href=["\']#["\']>(.*?)Marketing Automation(.*?)</a>', 
                                     r'<a href="marketing-automation.html">\1Marketing Automation\2</a>', text_content, flags=re.IGNORECASE | re.DOTALL)
                
                # Fix Login
                text_content = re.sub(r'<a([^>]+href=["\']#["\'][^>]*)>(.*?)Login(.*?)</a>', 
                                     r'<a\1 href="login.html">\2Login\3</a>', text_content, flags=re.IGNORECASE | re.DOTALL)
                text_content = re.sub(r'<a href=["\']#["\']>(.*?)Login(.*?)</a>', 
                                     r'<a href="login.html">\1Login\2</a>', text_content, flags=re.IGNORECASE | re.DOTALL)
                
                # Fix Signup / Try it Free
                for kw in ['Sign up', 'Sign Up', 'Try it Free']:
                    text_content = re.sub(r'<a([^>]+href=["\']#["\'][^>]*)>(.*?)' + kw + r'(.*?)</a>', 
                                         r'<a\1 href="signup.html">\2' + kw + r'\3</a>', text_content, flags=re.IGNORECASE | re.DOTALL)
                    text_content = re.sub(r'<a href=["\']#["\']>(.*?)' + kw + r'(.*?)</a>', 
                                         r'<a href="signup.html">\1' + kw + r'\2</a>', text_content, flags=re.IGNORECASE | re.DOTALL)
                
                return text_content

            new_content = patch_links(new_content)

            with open(filename, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {filename}")
            
        except Exception as e:
            print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    mega_fix()
