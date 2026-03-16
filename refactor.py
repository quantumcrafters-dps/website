import re

def refactor_html(filepath, is_past=False):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the <section> containing the members
    # It starts with `<section class="container mx-auto px-4 sm:px-6 lg:px-8 py-24 md:py-32">`
    # and ends with `<div class="watashino">` or `<div class="relative border-t`
    
    start_str = '<section class="container mx-auto px-4 sm:px-6 lg:px-8 py-24 md:py-32">'
    
    # In members.html there are two such sections. The second one is "Our Members". We should replace everything from the first section to the footer.
    # In past-members.html, there is only one.
    
    first_section_idx = content.find(start_str)
    if first_section_idx == -1:
        print("Could not find section in", filepath)
        return
        
    footer_idx = content.find('<div class="watashino">')
    if footer_idx == -1:
         footer_idx = content.find('<div class="relative border-t border-gray-400')
         
    if footer_idx == -1:
        print("Could not find footer in", filepath)
        return
        
    header = content[:first_section_idx]
    footer = content[footer_idx:]
    
    title = "Past Members" if is_past else "Our Members"
    subtitle = "Honoring the students who helped build and shape our IT Club community" if is_past else "Meet the talented students who make up our IT Club community"
    data_key = "past_members" if is_past else "current_members"
    
    dynamic_section = f'''        <section class="container mx-auto px-4 sm:px-6 lg:px-8 py-24 md:py-32">
            <div class="text-center space-y-4 mb-16 fade-in" data-delay="0">
                <h1 class="gradient-text hero-title text-4xl font-bold tracking-tight sm:text-5xl md:text-6xl">
                    {title}
                </h1>
                <p class="mx-auto max-w-2xl text-lg text-muted-foreground">
                    {subtitle}
                </p>
            </div>

            <div id="members-grid" class="mx-auto grid max-w-6xl grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
                <!-- Members will be loaded here dynamically -->
                <div class="col-span-1 md:col-span-2 lg:col-span-3 text-center py-12 text-muted-foreground" id="loading-message">
                    Loading members...
                </div>
            </div>
        </section>

        <script>
            document.addEventListener('DOMContentLoaded', async () => {{
                const grid = document.getElementById('members-grid');
                try {{
                    const res = await fetch('/api/members');
                    const data = await res.json();
                    
                    const members = data.{data_key} || [];
                    
                    if (members.length === 0) {{
                        grid.innerHTML = '<div class="col-span-1 md:col-span-2 lg:col-span-3 text-center py-12 text-muted-foreground">No members found.</div>';
                        return;
                    }}
                    
                    let html = '';
                    members.forEach((member, index) => {{
                        const defaultImg = 'data:image/svg+xml;utf8,<svg fill="%23999" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg"><path d="M16 15.503A5.041 5.041 0 1 0 16 5.42a5.041 5.041 0 0 0 0 10.083zm0 2.215c-6.703 0-11 3.699-11 5.5v3.363h22v-3.363c0-2.178-4.068-5.5-11-5.5z"></path></svg>';
                        const imgSrc = member.image || defaultImg;
                        const delay = (index % 3) * 100 + 100;
                        
                        html += `
                            <div class="member-card relative overflow-hidden rounded-lg border border-primary/20 bg-background p-6 hover:shadow-lg transition-shadow shadow-lg shadow-blue-500/10 fade-in stagger-animation" style="--delay: ${{delay}}ms; animation-play-state: running; opacity: 1; transform: none;">
                                <div class="absolute -inset-1 bg-gradient-to-r from-blue-500/10 via-blue-400/5 to-blue-500/10 rounded-lg blur-sm -z-10"></div>
                                <div class="flex items-center gap-4">
                                    <img src="${{imgSrc}}" alt="${{member.name}} profile" class="h-16 w-16 rounded-full object-cover border-2 border-primary/30" onerror="this.src='${{defaultImg}}'">
                                    <div class="flex-1 space-y-1">
                                        <h3 class="font-bold text-lg">${{member.name}}</h3>
                                        <p class="text-sm font-medium text-primary">${{member.role}}</p>
                                        <p class="text-sm text-muted-foreground">Class: ${{member.class}}</p>
                                        <p class="text-sm text-muted-foreground">Academic Year: ${{member.year}}</p>
                                    </div>
                                </div>
                            </div>
                        `;
                    }});
                    
                    grid.innerHTML = html;
                    
                }} catch (error) {{
                    grid.innerHTML = '<div class="col-span-1 md:col-span-2 lg:col-span-3 text-center py-12 text-red-500">Failed to load members. Please run the Python backend server.</div>';
                    console.error("Failed to load members:", error);
                }}
            }});
        </script>
'''

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(header + dynamic_section + footer)
        
    print(f"Refactored {filepath}")

refactor_html('c:/Users/Minu/Desktop/Anuj/Quantum-Crafters/website/members.html', is_past=False)
refactor_html('c:/Users/Minu/Desktop/Anuj/Quantum-Crafters/website/past-members.html', is_past=True)
