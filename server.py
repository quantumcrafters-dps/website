import http.server
import socketserver
import json
import os
import base64
import re

PORT = 8000
MEMBERS_FILE = 'members.json'
PUBLIC_DIR = 'public'

# MIME type -> file extension mapping
MIME_TO_EXT = {
    'image/jpeg': '.jpg',
    'image/jpg':  '.jpg',
    'image/png':  '.png',
    'image/gif':  '.gif',
    'image/webp': '.webp',
    'image/svg+xml': '.svg',
    'image/bmp':  '.bmp',
}

def sanitize_filename(name):
    """Remove unsafe characters and limit length."""
    name = os.path.basename(name)
    name = re.sub(r'[^\w\-.]', '_', name)
    return name[:120]

class MembersHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.end_headers()

    def do_GET(self):
        if self.path == '/api/members':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            if os.path.exists(MEMBERS_FILE):
                with open(MEMBERS_FILE, 'r', encoding='utf-8') as f:
                    self.wfile.write(f.read().encode('utf-8'))
            else:
                self.wfile.write(json.dumps({"current_members": [], "past_members": []}).encode('utf-8'))
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/api/members':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))

                # Strip any stray base64 blobs that slipped through - just in case
                for lst_key in ('current_members', 'past_members'):
                    for member in data.get(lst_key, []):
                        img = member.get('image', '')
                        if img.startswith('data:'):
                            # Upload it properly instead of saving the data URL in JSON
                            saved_path = self._save_data_url(img, member.get('id', 'member'))
                            member['image'] = saved_path if saved_path else ''

                with open(MEMBERS_FILE, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)

                # Also regenerate the static JS file for file:// access
                self._write_static_js(data)

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success"}).encode('utf-8'))

            except Exception as e:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))

        elif self.path == '/api/upload':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                filename = data.get('filename', 'upload')
                image_data = data.get('image_data', '')

                if not image_data:
                    raise ValueError("Missing image_data")

                saved_path = self._save_data_url(image_data, filename)
                if not saved_path:
                    raise ValueError("Could not save image")

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "filepath": saved_path}).encode('utf-8'))

            except Exception as e:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))

        else:
            self.send_response(404)
            self.end_headers()

    def _save_data_url(self, data_url, hint_filename):
        """
        Parse a data URL like  data:image/png;base64,<b64>
        Save the binary to public/<sanitized_name>.<ext>
        Return the relative path  public/<filename>  or None on failure.
        """
        try:
            # Parse  data:<mime>;base64,<data>
            header, b64_data = data_url.split(',', 1)
            # header looks like: data:image/png;base64
            parts = header.split(':', 1)
            mime_part = parts[1] if len(parts) > 1 else ''
            mime = mime_part.split(';')[0].strip().lower()
            ext = MIME_TO_EXT.get(mime, '')

            # Try to keep the original extension if valid
            base_name = os.path.splitext(sanitize_filename(hint_filename))[0]
            if not ext:
                # Fallback: use the extension from the hint filename
                hint_ext = os.path.splitext(hint_filename)[1].lower()
                ext = hint_ext if hint_ext else '.jpg'

            safe_name = base_name + ext
            os.makedirs(PUBLIC_DIR, exist_ok=True)
            filepath = os.path.join(PUBLIC_DIR, safe_name)

            image_bytes = base64.b64decode(b64_data)
            with open(filepath, 'wb') as f:
                f.write(image_bytes)

            return PUBLIC_DIR + '/' + safe_name
        except Exception:
            return None

    def _write_static_js(self, data):
        """Write members-data.js so public pages work via file:// (no server needed)."""
        try:
            js_content = (
                '// Auto-generated by server.py — do not edit manually.\n'
                '// Updated every time the Admin Panel saves changes.\n'
                'window.MEMBERS_DATA = ' + json.dumps(data, indent=2, ensure_ascii=False) + ';\n'
            )
            with open('members-data.js', 'w', encoding='utf-8') as f:
                f.write(js_content)
        except Exception as e:
            print(f'Warning: could not write members-data.js: {e}')

    def log_message(self, format, *args):
        # Suppress noisy access logs; only print errors
        if args and str(args[1]) not in ('200', '304'):
            super().log_message(format, *args)


os.chdir(os.path.dirname(os.path.abspath(__file__)))

with socketserver.TCPServer(("", PORT), MembersHTTPRequestHandler) as httpd:
    httpd.allow_reuse_address = True
    print(f"✅  API Server running at http://localhost:{PORT}")
    print("   Endpoints: GET/POST /api/members   POST /api/upload")
    httpd.serve_forever()
