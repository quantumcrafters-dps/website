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
            <!-- Dynamic Headers & Back Button -->
            <div class="text-center space-y-4 mb-16 fade-in" data-delay="0">
                <h1 id="page-title" class="gradient-text hero-title text-4xl font-bold tracking-tight sm:text-5xl md:text-6xl">
                    Our Departments
                </h1>
                <p id="page-subtitle" class="mx-auto max-w-2xl text-lg text-muted-foreground">
                    Click a department to see its team members.
                </p>
                <button id="back-to-depts" class="hidden px-4 py-2 bg-secondary text-secondary-foreground hover:bg-secondary/80 rounded-lg transition-colors mt-4">← Back to Departments</button>
            </div>

            <!-- VIEW A: The main grid showing all department options -->
            <div id="departments-grid" class="mx-auto grid max-w-6xl grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
                <div class="col-span-1 md:col-span-2 lg:col-span-3 text-center py-12 text-muted-foreground" id="loading-message">
                    Loading departments...
                </div>
            </div>

            <!-- VIEW B: Inside a Single Department (hidden by default) -->
            <div id="single-department-view" class="hidden max-w-6xl mx-auto space-y-12">
                <!-- Department Head Section -->
                <div class="text-center">
                    <span class="inline-block px-4 py-1.5 bg-primary/10 text-primary font-bold rounded-full text-sm border border-primary/20 mb-6 tracking-wider">DEPARTMENT HEAD</span>
                    <div id="dept-head-container" class="flex justify-center"></div>
                </div>
                
                <hr class="border-border/40 max-w-xl mx-auto">

                <!-- Regular Members Section -->
                <div>
                    <h2 class="text-center text-xl font-semibold text-muted-foreground mb-8">Team Members</h2>
                    <div id="dept-members-grid" class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3"></div>
                </div>
            </div>
        </section>

        <script>
            document.addEventListener('DOMContentLoaded', async () => {{
                const deptsGrid = document.getElementById('departments-grid');
                const singleDeptView = document.getElementById('single-department-view');
                const headContainer = document.getElementById('dept-head-container');
                const membersGrid = document.getElementById('dept-members-grid');
                const pageTitle = document.getElementById('page-title');
                const pageSubtitle = document.getElementById('page-subtitle');
                const backBtn = document.getElementById('back-to-depts');
                
                const defaultImg = 'data:image/svg+xml;utf8,<svg fill="%23999" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg"><path d="M16 15.503A5.041 5.041 0 1 0 16 5.42a5.041 5.041 0 0 0 0 10.083zm0 2.215c-6.703 0-11 3.699-11 5.5v3.363h22v-3.363c0-2.178-4.068-5.5-11-5.5z"></path></svg>';

                try {{
                    const res = await fetch('/api/members');
                    const data = await res.json();
                    const rawMembers = data.{data_key} || [];

                    if (rawMembers.length === 0) {{
                        deptsGrid.innerHTML = '<div class="col-span-1 md:col-span-2 lg:col-span-3 text-center py-12 text-muted-foreground">No members found.</div>';
                        return;
                    }}

                    // Group the members array by department dynamically!
                    const departments = {{}};
                    rawMembers.forEach(m => {{
                        const dName = m.department || "General Members";
                        if (!departments[dName]) {{
                            departments[dName] = {{ head: null, members: [] }};
                        }}
                        if (m.is_head) {{
                            departments[dName].head = m;
                        }} else {{
                            departments[dName].members.push(m);
                        }}
                    }});

                    // Function 1: Render the Department selection buttons
                    function showDepartmentsList() {{
                        pageTitle.textContent = "Our Departments";
                        pageSubtitle.textContent = "Click a department to see its team members.";
                        backBtn.classList.add('hidden');
                        singleDeptView.classList.add('hidden');
                        deptsGrid.classList.remove('hidden');

                        let html = '';
                        Object.keys(departments).forEach(deptName => {{
                            html += `
                                <div class="dept-select-card cursor-pointer relative overflow-hidden rounded-lg border border-primary/20 bg-background p-8 hover:shadow-lg text-center transition-all shadow-lg shadow-blue-500/10" data-dept="${{deptName}}">
                                    <h3 class="font-bold text-2xl mb-2">${{deptName}}</h3>
                                    <p class="text-sm text-primary font-medium">View Team Members →</p>
                                </div>
                            `;
                        }});
                        deptsGrid.innerHTML = html;

                        // Hook up click behaviors
                        document.querySelectorAll('.dept-select-card').forEach(card => {{
                            card.addEventListener('click', () => {{
                                showSingleDepartment(card.getAttribute('data-dept'));
                            }});
                        }});
                    }}

                    // Function 2: Render a specific chosen department view
                    function showSingleDepartment(deptName) {{
                        const dept = departments[deptName];
                        if (!dept) return;

                        pageTitle.textContent = deptName;
                        pageSubtitle.textContent = "Meet the team";
                        deptsGrid.classList.add('hidden');
                        backBtn.classList.remove('hidden');
                        singleDeptView.classList.remove('hidden');

                        const generateCardHTML = (m, index) => {{
                            const imgSrc = m.image || defaultImg;
                            const delay = (index % 3) * 100 + 100;
                            return `
                                <div class="member-card relative overflow-hidden rounded-lg border border-primary/20 bg-background p-6 hover:shadow-lg transition-shadow shadow-lg shadow-blue-500/10 fade-in stagger-animation" style="--delay: ${{delay}}ms; animation-play-state: running; opacity: 1; transform: none;">
                                    <div class="absolute -inset-1 bg-gradient-to-r from-blue-500/10 via-blue-400/5 to-blue-500/10 rounded-lg blur-sm -z-10"></div>
                                    <div class="flex items-center gap-4">
                                        <img src="${{imgSrc}}" alt="${{m.name}} profile" class="h-16 w-16 rounded-full object-cover border-2 border-primary/30" onerror="this.src='${{defaultImg}}'">
                                        <div class="flex-1 space-y-1 text-left">
                                            <h3 class="font-bold text-lg text-foreground">${{m.name}}</h3>
                                            <p class="text-sm font-medium text-primary">${{m.role}}</p>
                                            <p class="text-sm text-muted-foreground">Class: ${{m.class}}</p>
                                            <p class="text-sm text-muted-foreground">Academic Year: ${{m.year}}</p>
                                        </div>
                                    </div>
                                </div>
                            `;
                        }};

                        // Render head structure slot
                        if (dept.head) {{
                            headContainer.innerHTML = generateCardHTML(dept.head, 0);
                        }} else {{
                            headContainer.innerHTML = '<p class="text-muted-foreground text-sm py-4">No Department Head assigned yet.</p>';
                        }}

                        // Render underlying active team cards
                        let membersHtml = '';
                        dept.members.forEach((m, idx) => {{ membersHtml += generateCardHTML(m, idx); }});
                        membersGrid.innerHTML = membersHtml || '<p class="text-muted-foreground text-center col-span-full py-6">No core team members registered under this division.</p>';
                    }}

                    // Bind reverse flow button
                    backBtn.addEventListener('click', showDepartmentsList);
                    
                    // Kick off initialization
                    showDepartmentsList();

                }} catch (error) {{
                    deptsGrid.innerHTML = '<div class="col-span-1 md:col-span-2 lg:col-span-3 text-center py-12 text-red-500">Failed to load members. Please run the Python backend server.</div>';
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
