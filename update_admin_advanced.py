import codecs
import re

def rewrite_admin():
    filepath = 'c:/Users/Minu/Desktop/Anuj/Quantum-Crafters/website/admin.html'
    with codecs.open(filepath, 'r', 'utf-8') as f:
        content = f.read()

    # Find boundaries
    start_tag = '<section class="container mx-auto px-4 py-20 min-h-[60vh] flex flex-col items-center justify-center relative">'
    if start_tag not in content:
        start_tag = '<section class="container mx-auto px-4 py-20 min-h-[60vh] flex flex-col items-center justify-center">'
        
    start_idx = content.find(start_tag)
    end_tag = '</section>'
    end_idx = content.find(end_tag, start_idx) + len(end_tag)
    
    script_start = content.find('<script>', end_idx)
    script_end = content.find('</script>', script_start) + len('</script>')
    
    header = content[:start_idx]
    footer = content[script_end:]

    # New Admin Content
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
            <div id="admin-dashboard" class="w-full max-w-6xl hidden fade-in">
                <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
                    <div>
                        <h1 class="text-4xl font-bold gradient-text">Admin Dashboard</h1>
                        <p class="text-muted-foreground mt-2">Manage club members, edit details, upload images, and organize sections.</p>
                    </div>
                    <button onclick="logout()" class="px-4 py-2 border border-border hover:bg-secondary rounded-lg transition-colors flex items-center gap-2">
                        <i data-lucide="log-out" class="h-4 w-4"></i> Logout
                    </button>
                </div>
                
                <div id="api-error" class="bg-red-500/10 border border-red-500/50 text-red-500 p-4 rounded-lg mb-6 hidden">
                    Failed to connect to the server. Make sure you are running 'python server.py' and accessing the site via 'http://localhost:8000/'.
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    <!-- Current Members -->
                    <div class="bg-background border border-border/40 rounded-xl p-6 flex flex-col h-[700px]">
                        <h2 class="text-xl font-semibold mb-4 flex items-center justify-between">
                            Current Members
                            <button onclick="openMemberModal('current')" class="px-3 py-1 bg-primary text-primary-foreground rounded-md text-sm hover:bg-primary/90 flex items-center gap-1 shadow-md">
                                <i data-lucide="plus" class="h-4 w-4"></i> Add User
                            </button>
                        </h2>
                        <div class="space-y-3 overflow-y-auto pr-2 flex-grow scrollbar-thin" id="current-members-list">
                            <div class="text-center py-8 text-muted-foreground">Loading members...</div>
                        </div>
                    </div>
                    
                    <!-- Past Members -->
                    <div class="bg-background border border-border/40 rounded-xl p-6 flex flex-col h-[700px]">
                        <h2 class="text-xl font-semibold mb-4">Past Members</h2>
                        <div class="space-y-3 overflow-y-auto pr-2 flex-grow scrollbar-thin" id="past-members-list">
                            <div class="text-center py-8 text-muted-foreground">Loading past members...</div>
                        </div>
                    </div>
                </div>

            </div>

            <!-- Member Form Modal -->
            <div id="member-modal" class="fixed inset-0 z-50 bg-background/80 backdrop-blur-sm hidden flex-col items-center justify-center p-4">
                <div class="bg-card w-full max-w-lg border border-border/40 p-8 rounded-xl shadow-2xl relative max-h-[90vh] overflow-y-auto">
                    <button onclick="closeMemberModal()" class="absolute top-4 right-4 text-muted-foreground hover:text-foreground">
                        <i data-lucide="x" class="h-5 w-5"></i>
                    </button>
                    <h2 id="modal-title" class="text-2xl font-bold mb-6">Add Member</h2>
                    
                    <form id="member-form" onsubmit="submitForm(event)" class="space-y-5">
                        <input type="hidden" id="edit-id">
                        <input type="hidden" id="edit-list-type">
                        
                        <div>
                            <label class="block text-sm font-medium mb-1 text-muted-foreground">Full Name</label>
                            <input type="text" id="member-name" required class="w-full px-4 py-2 bg-secondary/30 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary text-foreground">
                        </div>
                        <div>
                            <label class="block text-sm font-medium mb-1 text-muted-foreground">Role</label>
                            <input type="text" id="member-role" required class="w-full px-4 py-2 bg-secondary/30 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary text-foreground" placeholder="e.g. Developer">
                        </div>
                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="block text-sm font-medium mb-1 text-muted-foreground">Class</label>
                                <input type="text" id="member-class" required class="w-full px-4 py-2 bg-secondary/30 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary text-foreground" placeholder="e.g. 11-A">
                            </div>
                            <div>
                                <label class="block text-sm font-medium mb-1 text-muted-foreground">Academic Year</label>
                                <input type="text" id="member-year" required class="w-full px-4 py-2 bg-secondary/30 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary text-foreground" placeholder="e.g. 2025-2026">
                            </div>
                        </div>
                        
                        <!-- Image Dropzone -->
                        <div>
                            <label class="block text-sm font-medium mb-1 text-muted-foreground">Profile Image</label>
                            <div id="dropzone" class="border-2 border-dashed border-border hover:border-primary/50 bg-secondary/10 rounded-xl p-6 text-center cursor-pointer transition-colors relative" onclick="document.getElementById('file-input').click()" ondragover="handleDragOver(event)" ondragleave="handleDragLeave(event)" ondrop="handleDrop(event)">
                                <input type="file" id="file-input" class="hidden" accept="image/*" onchange="handleFileSelect(event)">
                                <div id="dropzone-content" class="flex flex-col items-center pointer-events-none">
                                    <i data-lucide="upload-cloud" class="h-8 w-8 text-muted-foreground mb-2"></i>
                                    <p class="text-sm font-medium">Click to upload or drag & drop</p>
                                    <p class="text-xs text-muted-foreground mt-1">SVG, PNG, JPG or GIF (max. 2MB)</p>
                                </div>
                                <!-- Preview Image -->
                                <img id="image-preview" class="hidden absolute inset-0 w-full h-full object-contain p-2 rounded-xl bg-background" src="" alt="Preview">
                                <!-- Base64 / URL hidden store -->
                                <input type="hidden" id="member-img">
                            </div>
                            <button type="button" id="clear-img-btn" class="text-xs text-red-500 mt-2 hidden hover:underline" onclick="clearDropzone()">Remove Image</button>
                        </div>

                        <button type="submit" id="save-btn" class="w-full py-3 mt-4 bg-primary text-primary-foreground font-semibold rounded-lg hover:bg-primary/90 transition-colors shadow-lg">Save Member</button>
                    </form>
                </div>
            </div>

        </section>

        <script>
            let globalMembersData = { current_members: [], past_members: [] };

            // ---- Passcode Logic ----
            function checkPasscode() {
                const code = document.getElementById('passcode').value;
                if (code === 'admin123' || code === 'quantum2026') {
                    document.getElementById('passcode-screen').classList.add('hidden');
                    document.getElementById('admin-dashboard').classList.remove('hidden');
                    document.title = 'Admin Dashboard - Quantum Crafters';
                    fetchMembers();
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
                if (e.key === 'Enter') checkPasscode();
            });

            // ---- API Data Logic ----
            const API_URL = '/api/members';
            const UPLOAD_URL = '/api/upload';

            async function fetchMembers() {
                const errBox = document.getElementById('api-error');
                try {
                    const res = await fetch(API_URL);
                    if (!res.ok) throw new Error('API not available');
                    globalMembersData = await res.json();
                    errBox.classList.add('hidden');
                    renderMembers();
                } catch (e) {
                    errBox.classList.remove('hidden');
                }
            }

            async function saveToServer() {
                try {
                    const res = await fetch(API_URL, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(globalMembersData)
                    });
                    if (!res.ok) throw new Error('Failed to save');
                } catch (e) {
                    alert("Failed to save changes config to the server.");
                }
            }

            function renderMembers() {
                const currentEl = document.getElementById('current-members-list');
                const pastEl = document.getElementById('past-members-list');
                const defaultImg = 'data:image/svg+xml;utf8,<svg fill="%23999" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg"><path d="M16 15.503A5.041 5.041 0 1 0 16 5.42a5.041 5.041 0 0 0 0 10.083zm0 2.215c-6.703 0-11 3.699-11 5.5v3.363h22v-3.363c0-2.178-4.068-5.5-11-5.5z"></path></svg>';

                // Current Members
                currentEl.innerHTML = globalMembersData.current_members.map(m => `
                    <div class="flex items-center justify-between p-3 border border-border/40 rounded-xl bg-secondary/10 hover:bg-secondary/30 transition-colors group">
                        <div class="flex items-center gap-4">
                            <img src="${m.image || defaultImg}" class="w-12 h-12 rounded-full object-cover border-2 border-primary/20" onerror="this.src='${defaultImg}'">
                            <div>
                                <p class="font-medium flex items-center gap-2">${m.name}</p>
                                <p class="text-xs text-muted-foreground">${m.role} • ${m.class} • ${m.year}</p>
                            </div>
                        </div>
                        <div class="flex flex-col sm:flex-row gap-2 opacity-100 sm:opacity-0 sm:group-hover:opacity-100 transition-opacity">
                            <button onclick="editMember('current', '${m.id}')" class="px-2 py-1 bg-secondary hover:bg-secondary/70 rounded text-xs" title="Edit"><i data-lucide="edit-2" class="h-3.5 w-3.5"></i></button>
                            <button onclick="moveMember('${m.id}', 'current', 'past')" class="px-2 py-1 bg-blue-500/10 text-blue-400 hover:bg-blue-500/20 rounded text-xs" title="Move to Past Members"><i data-lucide="arrow-right-circle" class="h-3.5 w-3.5"></i></button>
                            <button onclick="deleteMember('${m.id}', 'current')" class="px-2 py-1 bg-red-500/10 text-red-500 hover:bg-red-500/20 rounded text-xs" title="Delete"><i data-lucide="trash-2" class="h-3.5 w-3.5"></i></button>
                        </div>
                    </div>
                `).join('') || '<div class="text-center py-8 text-muted-foreground">No current members.</div>';

                // Past Members
                pastEl.innerHTML = globalMembersData.past_members.map(m => `
                    <div class="flex items-center justify-between p-3 border border-border/40 rounded-xl bg-background/50 hover:bg-secondary/20 transition-colors opacity-80 group">
                        <div class="flex items-center gap-4">
                            <img src="${m.image || defaultImg}" class="w-12 h-12 rounded-full object-cover grayscale border-2 border-border" onerror="this.src='${defaultImg}'">
                            <div>
                                <p class="font-medium line-through decoration-muted-foreground/50">${m.name}</p>
                                <p class="text-xs text-muted-foreground">${m.role} • ${m.class} • ${m.year}</p>
                            </div>
                        </div>
                        <div class="flex flex-col sm:flex-row gap-2 opacity-100 sm:opacity-0 sm:group-hover:opacity-100 transition-opacity">
                            <button onclick="moveMember('${m.id}', 'past', 'current')" class="px-2 py-1 bg-green-500/10 text-green-400 hover:bg-green-500/20 rounded text-xs" title="Restore to Current Members"><i data-lucide="rotate-ccw" class="h-3.5 w-3.5"></i></button>
                            <button onclick="editMember('past', '${m.id}')" class="px-2 py-1 bg-secondary hover:bg-secondary/70 rounded text-xs" title="Edit"><i data-lucide="edit-2" class="h-3.5 w-3.5"></i></button>
                            <button onclick="deleteMember('${m.id}', 'past')" class="px-2 py-1 bg-red-500/10 text-red-500 hover:bg-red-500/20 rounded text-xs" title="Delete"><i data-lucide="trash-2" class="h-3.5 w-3.5"></i></button>
                        </div>
                    </div>
                `).join('') || '<div class="text-center py-8 text-muted-foreground">No past members.</div>';
                
                if(window.lucide) lucide.createIcons();
            }

            // ---- Action Logic ----
            async function moveMember(id, fromListStr, toListStr) {
                const fromList = fromListStr === 'current' ? globalMembersData.current_members : globalMembersData.past_members;
                const toList = toListStr === 'current' ? globalMembersData.current_members : globalMembersData.past_members;
                
                const idx = fromList.findIndex(m => m.id === id);
                if (idx > -1) {
                    const member = fromList.splice(idx, 1)[0];
                    toList.unshift(member); // Add to the top of the new list
                    await saveToServer();
                    renderMembers();
                }
            }

            async function deleteMember(id, listStr) {
                if(!confirm("Are you sure you want to delete this member permanently?")) return;
                
                const list = listStr === 'current' ? globalMembersData.current_members : globalMembersData.past_members;
                const idx = list.findIndex(m => m.id === id);
                if (idx > -1) {
                    list.splice(idx, 1);
                    await saveToServer();
                    renderMembers();
                }
            }

            // ---- Form / Modal Logic ----
            function openMemberModal(listType = 'current') {
                document.getElementById('member-form').reset();
                document.getElementById('edit-id').value = '';
                document.getElementById('edit-list-type').value = listType;
                document.getElementById('modal-title').textContent = 'Add New Member';
                clearDropzone();
                
                document.getElementById('member-modal').classList.remove('hidden');
                document.getElementById('member-modal').classList.add('flex');
            }

            function closeMemberModal() {
                document.getElementById('member-modal').classList.add('hidden');
                document.getElementById('member-modal').classList.remove('flex');
            }

            function editMember(listStr, id) {
                const list = listStr === 'current' ? globalMembersData.current_members : globalMembersData.past_members;
                const member = list.find(m => m.id === id);
                if(!member) return;

                document.getElementById('edit-id').value = member.id;
                document.getElementById('edit-list-type').value = listStr;
                document.getElementById('modal-title').textContent = 'Edit Member Details';
                
                document.getElementById('member-name').value = member.name;
                document.getElementById('member-role').value = member.role;
                document.getElementById('member-class').value = member.class;
                document.getElementById('member-year').value = member.year;
                
                if(member.image) {
                    setDropzonePreview(member.image);
                    document.getElementById('member-img').value = member.image; // It's just a path string
                } else {
                    clearDropzone();
                }

                document.getElementById('member-modal').classList.remove('hidden');
                document.getElementById('member-modal').classList.add('flex');
            }

            async function submitForm(e) {
                e.preventDefault();
                const btn = document.getElementById('save-btn');
                btn.textContent = "Saving...";
                btn.disabled = true;

                const editId = document.getElementById('edit-id').value;
                const listStr = document.getElementById('edit-list-type').value || 'current';
                const list = listStr === 'current' ? globalMembersData.current_members : globalMembersData.past_members;

                let finalImagePath = document.getElementById('member-img').value;
                
                // Need to upload?
                if (finalImagePath.startsWith('data:image')) {
                    try {
                        const nameForFile = document.getElementById('member-name').value.toLowerCase().replace(/[^a-z0-9]/g, '-');
                        const res = await fetch(UPLOAD_URL, {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                                filename: `${nameForFile}-${Date.now()}.png`,
                                image_data: finalImagePath
                            })
                        });
                        const uploadData = await res.json();
                        if (uploadData.status === 'success') {
                            finalImagePath = uploadData.filepath;
                        }
                    } catch (err) {
                        console.error("Image upload failed", err);
                    }
                }

                if (editId) {
                    // Update existing
                    const member = list.find(m => m.id === editId);
                    if (member) {
                        member.name = document.getElementById('member-name').value;
                        member.role = document.getElementById('member-role').value;
                        member.class = document.getElementById('member-class').value;
                        member.year = document.getElementById('member-year').value;
                        member.image = finalImagePath;
                    }
                } else {
                    // Create new
                    list.push({
                        id: Date.now().toString(),
                        name: document.getElementById('member-name').value,
                        role: document.getElementById('member-role').value,
                        class: document.getElementById('member-class').value,
                        year: document.getElementById('member-year').value,
                        image: finalImagePath
                    });
                }

                await saveToServer();
                renderMembers();
                
                closeMemberModal();
                btn.textContent = "Save Member";
                btn.disabled = false;
            }

            // ---- Image Drag & Drop Logic ----
            const dropzone = document.getElementById('dropzone');
            
            function handleDragOver(e) {
                e.preventDefault();
                dropzone.classList.add('border-primary', 'bg-primary/5');
            }
            function handleDragLeave(e) {
                e.preventDefault();
                dropzone.classList.remove('border-primary', 'bg-primary/5');
            }
            function handleDrop(e) {
                e.preventDefault();
                dropzone.classList.remove('border-primary', 'bg-primary/5');
                const file = e.dataTransfer.files[0];
                if (file && file.type.startsWith('image/')) processImageFile(file);
            }
            function handleFileSelect(e) {
                const file = e.target.files[0];
                if (file) processImageFile(file);
            }
            function processImageFile(file) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    const base64 = e.target.result;
                    setDropzonePreview(base64);
                };
                reader.readAsDataURL(file);
            }
            function setDropzonePreview(src) {
                document.getElementById('member-img').value = src;
                const preview = document.getElementById('image-preview');
                preview.src = src;
                preview.classList.remove('hidden');
                document.getElementById('dropzone-content').classList.add('hidden');
                document.getElementById('clear-img-btn').classList.remove('hidden');
            }
            function clearDropzone() {
                document.getElementById('member-img').value = '';
                document.getElementById('file-input').value = '';
                document.getElementById('image-preview').classList.add('hidden');
                document.getElementById('image-preview').src = '';
                document.getElementById('dropzone-content').classList.remove('hidden');
                document.getElementById('clear-img-btn').classList.add('hidden');
            }
        </script>
'''

    with codecs.open(filepath, 'w', 'utf-8') as f:
        f.write(header + new_admin_content + footer)
    print("Updated admin.html with Drag and drop and full CRUD")

rewrite_admin()
