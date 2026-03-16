import codecs
import re

def update_admin():
    filepath = 'c:/Users/Minu/Desktop/Anuj/Quantum-Crafters/website/admin.html'
    with codecs.open(filepath, 'r', 'utf-8') as f:
        content = f.read()

    # Find the boundary of the dynamic section
    start_tag = '<section class="container mx-auto px-4 py-20 min-h-[60vh] flex flex-col items-center justify-center">'
    end_tag = '</section>'
    
    start_idx = content.find(start_tag)
    # find the matching end_tag (the first </section> after start_tag)
    end_idx = content.find(end_tag, start_idx) + len(end_tag)
    
    # We also need to remove the existing <script> at the bottom before </body>
    # The existing script might be inside or after... Wait, our create_admin.py appended the script right after the section.
    # Let's find the script
    script_start = content.find('<script>', end_idx)
    script_end = content.find('</script>', script_start) + len('</script>')
    
    header = content[:start_idx]
    footer = content[script_end:]

    # New admin content injected with JS
    new_admin_content = '''
        <section class="container mx-auto px-4 py-20 min-h-[60vh] flex flex-col items-center justify-center relative">
            
            <!-- Passcode Screen -->
            <div id="passcode-screen" class="w-full max-w-md bg-background border border-border/40 p-8 rounded-xl shadow-2xl text-center fade-in">
                <div class="mb-6">
                    <i data-lucide="lock" class="h-12 w-12 mx-auto text-primary"></i>
                </div>
                <h1 class="text-3xl font-bold mb-2">Admin Access</h1>
                <p class="text-muted-foreground mb-8">Please enter the admin passcode to continue.</p>
                <div class="space-y-4">
                    <input type="password" id="passcode" class="w-full px-4 py-3 bg-secondary/50 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary text-center tracking-widest text-xl" placeholder="••••••••">
                    <button onclick="checkPasscode()" class="w-full py-3 bg-primary text-primary-foreground font-semibold rounded-lg hover:bg-primary/90 transition-colors">Unlock</button>
                    <p id="error-msg" class="text-red-500 text-sm hidden mt-2">Incorrect passcode. Try again.</p>
                </div>
            </div>

            <!-- Admin Dashboard -->
            <div id="admin-dashboard" class="w-full max-w-5xl hidden fade-in">
                <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
                    <div>
                        <h1 class="text-4xl font-bold gradient-text">Admin Dashboard</h1>
                        <p class="text-muted-foreground mt-2">Manage club members and send members to Past Members.</p>
                    </div>
                    <button onclick="logout()" class="px-4 py-2 border border-border hover:bg-secondary rounded-lg transition-colors flex items-center gap-2">
                        <i data-lucide="log-out" class="h-4 w-4"></i> Logout
                    </button>
                </div>
                
                <div id="api-error" class="bg-red-500/10 border border-red-500/50 text-red-500 p-4 rounded-lg mb-6 hidden">
                    Failed to connect to the server. Make sure you are running 'python server.py' and accessing the site via 'http://localhost:8000/'.
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                    <!-- Current Members -->
                    <div class="bg-background border border-border/40 rounded-xl p-6 flex flex-col h-[600px]">
                        <h2 class="text-xl font-semibold mb-4 flex items-center justify-between">
                            Current Members
                            <button onclick="openAddMemberModal()" class="px-3 py-1 bg-primary text-primary-foreground rounded-md text-sm hover:bg-primary/90 flex items-center gap-1">
                                <i data-lucide="plus" class="h-4 w-4"></i> Add User
                            </button>
                        </h2>
                        <div class="space-y-3 overflow-y-auto pr-2 flex-grow" id="current-members-list">
                            <div class="text-center py-8 text-muted-foreground">Loading members...</div>
                        </div>
                    </div>
                    
                    <!-- Past Members -->
                    <div class="bg-background border border-border/40 rounded-xl p-6 flex flex-col h-[600px]">
                        <h2 class="text-xl font-semibold mb-4">Past Members</h2>
                        <div class="space-y-3 overflow-y-auto pr-2 flex-grow" id="past-members-list">
                            <div class="text-center py-8 text-muted-foreground">Loading past members...</div>
                        </div>
                    </div>
                </div>

            </div>

            <!-- Add Member Modal -->
            <div id="add-member-modal" class="fixed inset-0 z-50 bg-background/80 backdrop-blur-sm hidden flex-col items-center justify-center p-4">
                <div class="bg-card w-full max-w-md border border-border/40 p-6 rounded-xl shadow-2xl relative">
                    <button onclick="closeAddMemberModal()" class="absolute top-4 right-4 text-muted-foreground hover:text-foreground">
                        <i data-lucide="x" class="h-5 w-5"></i>
                    </button>
                    <h2 class="text-2xl font-bold mb-6">Add New Member</h2>
                    
                    <form id="add-member-form" onsubmit="submitNewMember(event)" class="space-y-4">
                        <div>
                            <label class="block text-sm font-medium mb-1 text-muted-foreground">Full Name</label>
                            <input type="text" id="new-name" required class="w-full px-3 py-2 bg-secondary/50 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary text-foreground">
                        </div>
                        <div>
                            <label class="block text-sm font-medium mb-1 text-muted-foreground">Role</label>
                            <input type="text" id="new-role" required class="w-full px-3 py-2 bg-secondary/50 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary text-foreground" placeholder="e.g. Developer">
                        </div>
                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="block text-sm font-medium mb-1 text-muted-foreground">Class</label>
                                <input type="text" id="new-class" required class="w-full px-3 py-2 bg-secondary/50 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary text-foreground" placeholder="e.g. 11-A">
                            </div>
                            <div>
                                <label class="block text-sm font-medium mb-1 text-muted-foreground">Academic Year</label>
                                <input type="text" id="new-year" required class="w-full px-3 py-2 bg-secondary/50 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary text-foreground" placeholder="e.g. 2025-2026">
                            </div>
                        </div>
                        <div>
                            <label class="block text-sm font-medium mb-1 text-muted-foreground">Image URL (Optional)</label>
                            <input type="text" id="new-img" class="w-full px-3 py-2 bg-secondary/50 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary text-foreground" placeholder="public/image.png">
                        </div>
                        <button type="submit" id="save-btn" class="w-full py-3 mt-4 bg-primary text-primary-foreground font-semibold rounded-lg hover:bg-primary/90 transition-colors">Save Member</button>
                    </form>
                </div>
            </div>

        </section>

        <script>
            let globalMembersData = {
                current_members: [],
                past_members: []
            };

            // ---- Passcode Logic ----
            function checkPasscode() {
                const code = document.getElementById('passcode').value;
                if (code === 'admin123' || code === 'quantum2026') {
                    document.getElementById('passcode-screen').classList.add('hidden');
                    document.getElementById('admin-dashboard').classList.remove('hidden');
                    document.title = 'Admin Dashboard - Quantum Crafters';
                    fetchMembers(); // Load the database
                } else {
                    document.getElementById('error-msg').classList.remove('hidden');
                }
            }

            function logout() {
                document.getElementById('passcode').value = '';
                document.getElementById('passcode-screen').classList.remove('hidden');
                document.getElementById('admin-dashboard').classList.add('hidden');
                document.getElementById('error-msg').classList.add('hidden');
            }

            document.getElementById('passcode').addEventListener('keypress', function (e) {
                if (e.key === 'Enter') {
                    checkPasscode();
                }
            });

            // ---- API Logic ----
            const API_URL = '/api/members';

            async function fetchMembers() {
                const currentEl = document.getElementById('current-members-list');
                const pastEl = document.getElementById('past-members-list');
                const errBox = document.getElementById('api-error');
                
                try {
                    const res = await fetch(API_URL);
                    if (!res.ok) throw new Error('API not available');
                    globalMembersData = await res.json();
                    
                    errBox.classList.add('hidden');
                    renderMembers();
                } catch (e) {
                    console.error(e);
                    errBox.classList.remove('hidden');
                    currentEl.innerHTML = '<div class="text-red-500 text-center py-4">Error loading data.</div>';
                    pastEl.innerHTML = '<div class="text-red-500 text-center py-4">Error loading data.</div>';
                }
            }

            async function saveToServer() {
                try {
                    const res = await fetch(API_URL, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(globalMembersData)
                    });
                    if (!res.ok) throw new Error('Failed to save');
                } catch (e) {
                    alert("Failed to save changes to the server. Make sure the server.py is running.");
                    console.error(e);
                }
            }

            function renderMembers() {
                const currentEl = document.getElementById('current-members-list');
                const pastEl = document.getElementById('past-members-list');
                
                const defaultImg = 'data:image/svg+xml;utf8,<svg fill="%23999" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg"><path d="M16 15.503A5.041 5.041 0 1 0 16 5.42a5.041 5.041 0 0 0 0 10.083zm0 2.215c-6.703 0-11 3.699-11 5.5v3.363h22v-3.363c0-2.178-4.068-5.5-11-5.5z"></path></svg>';

                // Render Current Members
                if (globalMembersData.current_members.length === 0) {
                    currentEl.innerHTML = '<div class="text-center py-8 text-muted-foreground border border-dashed border-border/50 rounded-lg">No current members.</div>';
                } else {
                    currentEl.innerHTML = globalMembersData.current_members.map(m => `
                        <div class="flex items-center justify-between p-3 border border-border/40 rounded-lg bg-secondary/10 hover:bg-secondary/30 transition-colors">
                            <div class="flex items-center gap-3">
                                <img src="${m.image || defaultImg}" class="w-10 h-10 rounded-full object-cover border border-primary/20" onerror="this.src='${defaultImg}'">
                                <div>
                                    <p class="font-medium flex items-center gap-2">${m.name} <span class="text-[10px] uppercase bg-primary/20 text-primary px-1.5 py-0.5 rounded">${m.role}</span></p>
                                    <p class="text-xs text-muted-foreground">${m.class} | ${m.year}</p>
                                </div>
                            </div>
                            <button onclick="moveToPast('${m.id}')" class="px-3 py-1.5 text-xs text-muted-foreground hover:bg-background hover:text-foreground border border-transparent hover:border-border/50 rounded-md transition-all shadow-sm">
                                Move to Past
                            </button>
                        </div>
                    `).join('');
                }

                // Render Past Members
                if (globalMembersData.past_members.length === 0) {
                    pastEl.innerHTML = '<div class="text-center py-8 text-muted-foreground border border-dashed border-border/50 rounded-lg">No past members yet.</div>';
                } else {
                    pastEl.innerHTML = globalMembersData.past_members.map(m => `
                        <div class="flex items-center justify-between p-3 border border-border/40 rounded-lg bg-background/50 opacity-80">
                            <div class="flex items-center gap-3">
                                <img src="${m.image || defaultImg}" class="w-10 h-10 rounded-full object-cover grayscale border border-border" onerror="this.src='${defaultImg}'">
                                <div>
                                    <p class="font-medium">${m.name}</p>
                                    <p class="text-xs text-muted-foreground">${m.role} (${m.year})</p>
                                </div>
                            </div>
                            <!-- You could add a Delete/Restore button here if needed in the future -->
                        </div>
                    `).join('');
                }
                
                // Refresh lucide icons if there are new ones injected
                if(window.lucide) { lucide.createIcons(); }
            }

            // ---- Create/Update Logic ----
            function openAddMemberModal() {
                document.getElementById('add-member-form').reset();
                document.getElementById('add-member-modal').classList.remove('hidden');
                document.getElementById('add-member-modal').classList.add('flex');
            }

            function closeAddMemberModal() {
                document.getElementById('add-member-modal').classList.add('hidden');
                document.getElementById('add-member-modal').classList.remove('flex');
            }

            async function submitNewMember(e) {
                e.preventDefault();
                const btn = document.getElementById('save-btn');
                btn.textContent = "Saving...";
                btn.disabled = true;

                const newMember = {
                    id: Date.now().toString(),
                    name: document.getElementById('new-name').value,
                    role: document.getElementById('new-role').value,
                    class: document.getElementById('new-class').value,
                    year: document.getElementById('new-year').value,
                    image: document.getElementById('new-img').value || ""
                };

                globalMembersData.current_members.push(newMember);
                await saveToServer();
                renderMembers();
                
                closeAddMemberModal();
                btn.textContent = "Save Member";
                btn.disabled = false;
            }

            async function moveToPast(id) {
                const idx = globalMembersData.current_members.findIndex(m => m.id === id);
                if (idx > -1) {
                    const member = globalMembersData.current_members.splice(idx, 1)[0];
                    globalMembersData.past_members.unshift(member); // add to top
                    await saveToServer();
                    renderMembers();
                }
            }
        </script>
'''

    with codecs.open(filepath, 'w', 'utf-8') as f:
        f.write(header + new_admin_content + footer)
    print("Updated admin.html with full dynamic backend API")

update_admin()
