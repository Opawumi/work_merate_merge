import glob
import re
import os

def mega_fix():
    # 1. Read the master navbar from index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        master_content = f.read()
    
    # Extract nav block
    nav_match = re.search(r'(<nav.*?</nav>)', master_content, re.DOTALL)
    if not nav_match:
        print("Could not find navbar in index.html")
        return
    
    master_nav = nav_match.group(1)
    
    # Identify todos: remove page-specific active classes if any (e.g. if I missed any)
    # The master_nav should be "clean".
    
    html_files = [f for f in glob.glob('*.html') if f != 'index.html' and f != 'check_links.py' and f != 'mega_fix.py']
    
    for filename in html_files:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 2. Replace the navbar
            new_content = re.sub(r'<nav.*?</nav>', master_nav, content, flags=re.DOTALL)
            
            # 3. Patch the active link for THIS page specifically if it exists in the new_content
            # Check for <a href="filename" ...
            # Actually, let's just do a simple highlight for the main nav links if the href matches filename
            # This is a bit tricky with the mega-dropdown, but we can try.
            # However, the user didn't ask for it, so let's stick to the core task: "same mega-dropdown".
            
            # 4. Fix footer links that are broken (href="#")
            # Marketing Automation
            new_content = re.sub(r'(<a[^>]+href=["\'])#?["\'][^>]*>(.*?)Marketing Automation(.*?)</a>', 
                                 r'\1marketing-automation.html\2Marketing Automation\3</a>', 
                                 new_content, flags=re.IGNORECASE | re.DOTALL)
            
            # Login
            new_content = re.sub(r'(<a[^>]+href=["\'])#?["\'][^>]*>(.*?)Login(.*?)</a>', 
                                 r'\1login.html\2Login\3</a>', 
                                 new_content, flags=re.IGNORECASE | re.DOTALL)
            
            # Sign up / Try it Free
            new_content = re.sub(r'(<a[^>]+href=["\'])#?["\'][^>]*>(.*?)Sign up(.*?)</a>', 
                                 r'\1signup.html\2Sign up\3</a>', 
                                 new_content, flags=re.IGNORECASE | re.DOTALL)
            new_content = re.sub(r'(<a[^>]+href=["\'])#?["\'][^>]*>(.*?)Sign Up(.*?)</a>', 
                                 r'\1signup.html\2Sign Up\3</a>', 
                                 new_content, flags=re.IGNORECASE | re.DOTALL)
            new_content = re.sub(r'(<a[^>]+href=["\'])#?["\'][^>]*>(.*?)Try it Free(.*?)</a>', 
                                 r'\1signup.html\2Try it Free\3</a>', 
                                 new_content, flags=re.IGNORECASE | re.DOTALL)
            
            # Also fix marketing-automation.html if it has # for itself? Yes, the script will catch it.
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {filename}")
            
        except Exception as e:
            print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    mega_fix()
