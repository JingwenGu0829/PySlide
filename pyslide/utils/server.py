"""
Server utilities for PySlide.
"""

import os
import tempfile
import webbrowser
import shutil
from http.server import HTTPServer, SimpleHTTPRequestHandler
from typing import Dict, Any
from pathlib import Path

class PySlideHandler(SimpleHTTPRequestHandler):
    """Custom handler for serving PySlide content"""
    def __init__(self, *args, **kwargs):
        self.static_files = kwargs.pop('static_files', {})
        super().__init__(*args, **kwargs)

    def do_GET(self):
        # 如果请求的是静态文件
        if self.path in self.static_files:
            self.send_response(200)
            if self.path.endswith('.png'):
                self.send_header('Content-type', 'image/png')
            elif self.path.endswith('.jpg') or self.path.endswith('.jpeg'):
                self.send_header('Content-type', 'image/jpeg')
            elif self.path.endswith('.gif'):
                self.send_header('Content-type', 'image/gif')
            self.end_headers()
            
            with open(self.static_files[self.path], 'rb') as f:
                self.wfile.write(f.read())
            return
        
        return super().do_GET()

def serve_presentation(html_content: str, static_files: Dict[str, str] = None, port: int = 8000) -> None:
    """Serve the presentation on a local HTTP server.
    
    Args:
        html_content: The HTML content to serve
        static_files: Dictionary mapping URL paths to file paths
        port: Port number to serve on
    """
    # Create temporary directory for serving files
    temp_dir = tempfile.mkdtemp()
    html_path = os.path.join(temp_dir, 'index.html')
    
    # Write HTML file
    with open(html_path, 'w') as f:
        f.write(html_content)
    
    # Change to temp directory
    os.chdir(temp_dir)
    
    # Create handler with static files
    handler = lambda *args: PySlideHandler(*args, static_files=static_files or {})
    
    # Start server
    server = HTTPServer(('localhost', port), handler)
    print(f"Starting presentation at http://localhost:{port}")
    
    # Open browser
    webbrowser.open(f'http://localhost:{port}')
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.shutdown()
    finally:
        # Clean up temporary directory
        shutil.rmtree(temp_dir) 