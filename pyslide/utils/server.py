"""
Server utilities for PySlide.
"""

import os
import tempfile
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
from typing import Dict, Any

def serve_presentation(html_content: str, port: int = 8000) -> None:
    """Serve the presentation on a local HTTP server."""
    # Create temporary directory for serving files
    temp_dir = tempfile.mkdtemp()
    html_path = os.path.join(temp_dir, 'index.html')
    
    # Write HTML file
    with open(html_path, 'w') as f:
        f.write(html_content)
    
    # Change to temp directory
    os.chdir(temp_dir)
    
    # Start server
    server = HTTPServer(('localhost', port), SimpleHTTPRequestHandler)
    print(f"Starting presentation at http://localhost:{port}")
    
    # Open browser
    webbrowser.open(f'http://localhost:{port}')
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.shutdown() 