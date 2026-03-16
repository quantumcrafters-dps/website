import codecs

with codecs.open('c:/Users/Minu/Desktop/Anuj/Quantum-Crafters/website/about.html', 'r', 'utf-8') as f:
    t = f.read()

header_end = t.find('<main>')
if header_end == -1:
    header_end = t.find('<section')

footer_start = t.find('<footer')
if footer_start == -1:
    footer_start = t.find('<div class="relative border-t border-gray-400/20')

header = t[:header_end]
header = header.replace('<title>About Us- Quantum Crafters</title>', '<title>Admin Dashboard - Quantum Crafters</title>')
footer = t[footer_start:]

admin_content = '''
        <section class="container mx-auto px-4 py-20 min-h-[60vh] flex flex-col items-center justify-center">
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

            <div id="admin-dashboard" class="w-full max-w-5xl hidden fade-in">
                <div class="flex justify-between items-center mb-8">
                    <div>
                        <h1 class="text-4xl font-bold gradient-text">Admin Dashboard</h1>
                        <p class="text-muted-foreground mt-2">Manage club members and send members to Past Members.</p>
                    </div>
                    <button onclick="logout()" class="px-4 py-2 border border-border hover:bg-secondary rounded-lg transition-colors flex items-center gap-2">
                        <i data-lucide="log-out" class="h-4 w-4"></i> Logout
                    </button>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                    <!-- Current Members -->
                    <div class="bg-background border border-border/40 rounded-xl p-6">
                        <h2 class="text-xl font-semibold mb-4 flex items-center justify-between">
                            Current Members
                            <button class="px-3 py-1 bg-primary text-primary-foreground rounded-md text-sm hover:bg-primary/90">+ Add User</button>
                        </h2>
                        <div class="space-y-3">
                            <div class="flex items-center justify-between p-3 border border-border/40 rounded-lg bg-secondary/20">
                                <div class="flex items-center gap-3">
                                    <div class="w-10 h-10 bg-primary/20 rounded-full flex items-center justify-center"><i data-lucide="user" class="h-5 w-5 text-primary"></i></div>
                                    <div>
                                        <p class="font-medium">Ankit Mohapatra</p>
                                        <p class="text-xs text-muted-foreground">Council Member</p>
                                    </div>
                                </div>
                                <button onclick="moveToPast(this, 'Ankit Mohapatra')" class="px-3 py-1 text-xs border border-blue-500/30 text-blue-400 hover:bg-blue-500/10 rounded-md transition-colors whitespace-nowrap">Move to Past</button>
                            </div>
                            
                            <div class="flex items-center justify-between p-3 border border-border/40 rounded-lg bg-secondary/20">
                                <div class="flex items-center gap-3">
                                    <div class="w-10 h-10 bg-primary/20 rounded-full flex items-center justify-center"><i data-lucide="user" class="h-5 w-5 text-primary"></i></div>
                                    <div>
                                        <p class="font-medium">Shreyansh Sagar</p>
                                        <p class="text-xs text-muted-foreground">Council Member</p>
                                    </div>
                                </div>
                                <button onclick="moveToPast(this, 'Shreyansh Sagar')" class="px-3 py-1 text-xs border border-blue-500/30 text-blue-400 hover:bg-blue-500/10 rounded-md transition-colors whitespace-nowrap">Move to Past</button>
                            </div>
                            
                            <p class="text-center text-sm text-muted-foreground pt-4">Mock UI — Use a backend to manage actual data.</p>
                        </div>
                    </div>
                    
                    <!-- Past Members -->
                    <div class="bg-background border border-border/40 rounded-xl p-6">
                        <h2 class="text-xl font-semibold mb-4">Past Members</h2>
                        <div class="space-y-3" id="past-members-list">
                            <div class="flex items-center gap-3 p-3 border border-border/40 rounded-lg bg-secondary/10 opacity-70">
                                <div class="w-10 h-10 bg-gray-500/20 rounded-full flex items-center justify-center"><i data-lucide="history" class="h-5 w-5 text-gray-400"></i></div>
                                <div>
                                    <p class="font-medium">Pranav</p>
                                    <p class="text-xs text-muted-foreground">Alumni (2024)</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        </section>

        <script>
            function checkPasscode() {
                // simple lock
                const code = document.getElementById('passcode').value;
                if (code === 'admin123' || code === 'quantum2026') {
                    document.getElementById('passcode-screen').classList.add('hidden');
                    document.getElementById('admin-dashboard').classList.remove('hidden');
                    document.title = 'Admin Dashboard - Quantum Crafters';
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

            function moveToPast(buttonElement, name) {
                alert(`Mock Logic: Successfully moved ${name} to Past Members!\\n\\nNote: Since this is a static website front-end, the change will not save permanently. A backend database is required for actual logic.`);
                
                // Remove from current list visually
                buttonElement.parentElement.remove();
                
                // Add to past members list visually
                const list = document.getElementById('past-members-list');
                const html = `
                <div class="flex items-center gap-3 p-3 border border-border/40 rounded-lg bg-secondary/10 opacity-70">
                    <div class="w-10 h-10 bg-gray-500/20 rounded-full flex items-center justify-center"><i data-lucide="history" class="h-5 w-5 text-gray-400"></i></div>
                    <div>
                        <p class="font-medium">${name}</p>
                        <p class="text-xs text-muted-foreground">Moved to Past Members</p>
                    </div>
                </div>`;
                list.insertAdjacentHTML('afterbegin', html);
            }
            
            // Allow enter key to submit passcode
            document.getElementById('passcode').addEventListener('keypress', function (e) {
                if (e.key === 'Enter') {
                    checkPasscode();
                }
            });
        </script>
'''

with codecs.open('c:/Users/Minu/Desktop/Anuj/Quantum-Crafters/website/admin.html', 'w', 'utf-8') as f:
    f.write(header)
    f.write(admin_content)
    f.write(footer)

print('Admin page created')
