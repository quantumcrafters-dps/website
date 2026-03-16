import os
import glob
import re

files = glob.glob('c:/Users/Minu/Desktop/Anuj/Quantum-Crafters/website/*.html')

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the members link and append past-members and admin.html
    # We only want to target the footer links. They have this specific class:
    target_class = 'class="text-muted-foreground transition-colors hover:text-primary hover-plain"'
    
    # Check if we already have Admin Panel link to avoid duplication
    if 'Admin Panel' in content:
        continue
        
    # Regex to match the Members link in the footer
    # It can be href="members.html" or href="#"
    pattern = r'(<li>\s*<a href="[^"]*"\s+' + re.escape(target_class) + r'>Members</a>\s*</li>)'
    
    new_links = f"""
                                <li><a href="past-members.html" {target_class}>Past Members</a></li>
                                <li><a href="admin.html" {target_class}>Admin Panel</a></li>"""
                                
    # Notice: In past-members.html, we already manually added Past Members link.
    # So if there's already a Past Members link, we should only add Admin Panel.
    if 'Past Members</a>' in content and 'admin.html' not in content:
        # Just add admin.html after Past Members
        pm_pattern = r'(<li>\s*<a href="past-members\.html"\s+' + re.escape(target_class) + r'>Past Members</a>\s*</li>)'
        content = re.sub(pm_pattern, r'\1\n' + f'                                <li><a href="admin.html" {target_class}>Admin Panel</a></li>', content)
    else:
        # Add both after Members
        content = re.sub(pattern, r'\1\n' + new_links, content)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Footers updated!")
