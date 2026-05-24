"""
Enhanced HTTP Server with Auto-Reload Detection
Monitors file changes and notifies users to refresh browser
"""

import http.server
import socketserver
import os
import sys
import threading
import time
from pathlib import Path

# Configuration
PORT = 8080
WATCH_DIR = "web"
RELOAD_DELAY = 1  # seconds

class AutoReloadHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP handler with auto-reload support"""
    
    def end_headers(self):
        # Add cache control headers for development
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()
    
    def log_message(self, format, *args):
        # Colorize log messages
        timestamp = time.strftime('%H:%M:%S')
        print(f"\033[90m[{timestamp}]\033[0m {format % args}")

def watch_for_changes():
    """Monitor directory for file changes"""
    import hashlib
    
    def get_file_hashes():
        """Get hashes of all files in watch directory"""
        hashes = {}
        watch_path = Path(WATCH_DIR)
        for file_path in watch_path.rglob('*'):
            if file_path.is_file() and not file_path.name.startswith('.'):
                try:
                    with open(file_path, 'rb') as f:
                        hashes[str(file_path)] = hashlib.md5(f.read()).hexdigest()
                except:
                    pass
        return hashes
    
    print(f"\n👀 Watching for changes in {WATCH_DIR}/ directory...")
    print("   (Auto-reload detection enabled)\n")
    
    old_hashes = get_file_hashes()
    
    while True:
        time.sleep(RELOAD_DELAY)
        new_hashes = get_file_hashes()
        
        # Check for changes
        changed = False
        for file_path, new_hash in new_hashes.items():
            if file_path not in old_hashes:
                print(f"\n✨ New file detected: {file_path}")
                changed = True
            elif old_hashes[file_path] != new_hash:
                print(f"\n📝 File changed: {file_path}")
                changed = True
        
        for file_path in old_hashes:
            if file_path not in new_hashes:
                print(f"\n🗑️ File removed: {file_path}")
                changed = True
        
        if changed:
            print("   💡 Refresh your browser to see changes!\n")
        
        old_hashes = new_hashes

def start_server():
    """Start the HTTP server"""
    os.chdir(WATCH_DIR)
    
    with socketserver.TCPServer(("", PORT), AutoReloadHandler) as httpd:
        print("=" * 50)
        print("  DSA Study Plan - Web Server")
        print("=" * 50)
        print(f"\n🌐 Server running at: http://localhost:{PORT}")
        print(f"📁 Serving files from: {WATCH_DIR}/")
        print(f"\n💡 Open the URL in your browser")
        print(f"🛑 Press Ctrl+C to stop the server\n")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n🛑 Server stopped")
            httpd.shutdown()

if __name__ == "__main__":
    # Start file watcher in background
    watcher_thread = threading.Thread(target=watch_for_changes, daemon=True)
    watcher_thread.start()
    
    # Start server in main thread
    start_server()
