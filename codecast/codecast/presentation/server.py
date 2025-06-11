"""
Web server for interactive code execution presentations.
"""

import os
import tempfile
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from typing import Dict, Any, Optional

class PresentationServer:
    """Simple HTTP server for serving code execution presentations."""
    
    def __init__(self, template_dir: Optional[str] = None):
        self.template_dir = template_dir or str(Path(__file__).parent / 'templates')
    
    def serve_presentation(self, presentation_data: str, port: int = 8000):
        """Serve presentation on local HTTP server.
        
        Args:
            presentation_data: JSON presentation data
            port: Port to serve on (default: 8000)
        """
        # Create HTML content
        html_content = self._create_html_content(presentation_data)
        
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
        print(f"Starting server at http://localhost:{port}")
        
        # Open browser
        webbrowser.open(f'http://localhost:{port}')
        
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            server.shutdown()
    
    def _create_html_content(self, presentation_data: str) -> str:
        """Create HTML content with embedded presentation data."""
        template_path = Path(self.template_dir) / 'presentation.html'
        if not template_path.exists():
            # Use default template if custom template doesn't exist
            return self._get_default_template().replace('PRESENTATION_DATA_PLACEHOLDER', presentation_data)
        
        # Use custom template
        template = template_path.read_text()
        return template.replace('PRESENTATION_DATA_PLACEHOLDER', presentation_data)
    
    def _get_default_template(self) -> str:
        """Get default HTML template."""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>CodeCast Visualization</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
                pre { background: #f5f5f5; padding: 10px; border-radius: 4px; }
                .visualization { margin: 20px 0; }
                .timeline { position: relative; height: 200px; margin: 20px 0; }
                .event { position: absolute; cursor: pointer; }
                .call-stack { border-left: 2px solid #666; padding-left: 20px; }
            </style>
            <script>
                // Parse and display the presentation data
                const presentationData = PRESENTATION_DATA_PLACEHOLDER;
                
                function displayPresentation() {
                    const container = document.getElementById('presentation');
                    
                    // Display source code
                    const codeSection = document.createElement('div');
                    codeSection.innerHTML = `
                        <h2>Source Code</h2>
                        <pre>${presentationData.trace.source_code}</pre>
                    `;
                    container.appendChild(codeSection);
                    
                    // Display execution trace
                    const traceSection = document.createElement('div');
                    traceSection.innerHTML = '<h2>Execution Trace</h2>';
                    presentationData.trace.events.forEach(event => {
                        traceSection.innerHTML += `
                            <div class="event">
                                <strong>Line ${event.line_number}</strong> - ${event.event_type}
                                ${event.output ? `<br>Output: ${event.output}` : ''}
                                ${event.exception ? `<br>Exception: ${event.exception}` : ''}
                            </div>
                        `;
                    });
                    container.appendChild(traceSection);
                    
                    // Display visualizations
                    if (presentationData.visualizations) {
                        const visSection = document.createElement('div');
                        visSection.innerHTML = '<h2>Visualizations</h2>';
                        
                        // Variable timeline
                        if (presentationData.visualizations.variables) {
                            visSection.innerHTML += `
                                <div class="visualization">
                                    <h3>Variable Timeline</h3>
                                    <div class="timeline" id="variable-timeline"></div>
                                </div>
                            `;
                        }
                        
                        // Call stack
                        if (presentationData.visualizations.callstack) {
                            visSection.innerHTML += `
                                <div class="visualization">
                                    <h3>Call Stack</h3>
                                    <div class="call-stack" id="call-stack"></div>
                                </div>
                            `;
                        }
                        
                        container.appendChild(visSection);
                    }
                }
                
                // Initialize when page loads
                window.onload = displayPresentation;
            </script>
        </head>
        <body>
            <h1>CodeCast Visualization</h1>
            <div id="presentation"></div>
        </body>
        </html>
        """ 