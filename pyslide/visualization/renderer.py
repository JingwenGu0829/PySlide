"""
HTML rendering functionality for PySlide.
"""

from typing import Dict, Any
import json

def create_html_content(presentation_data: Dict[str, Any]) -> str:
    """Create HTML content with embedded presentation data."""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>PySlide Presentation</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/styles/github.min.css">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/highlight.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/languages/python.min.js"></script>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin: 0;
                padding: 20px;
                line-height: 1.6;
                color: #333;
                background: #f5f5f5;
            }}
            .slide {{
                margin-bottom: 40px;
                padding: 20px;
                border: 1px solid #e9ecef;
                border-radius: 8px;
                background: white;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .slide-title {{
                margin: 0 0 10px;
                color: #2c3e50;
                font-size: 24px;
            }}
            .slide-description {{
                color: #666;
                margin-bottom: 20px;
            }}
            pre {{
                background: #f8f9fa;
                padding: 15px;
                border-radius: 5px;
                overflow-x: auto;
                border: 1px solid #e9ecef;
                margin: 10px 0;
            }}
            .annotation {{
                margin: 5px 0;
                padding: 5px 10px;
                background: #fff3cd;
                border-left: 4px solid #ffc107;
                border-radius: 3px;
            }}
            .visualization {{
                margin: 20px 0;
                padding: 15px;
                background: white;
                border-radius: 5px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .execution-output {{
                margin: 10px 0;
                padding: 10px;
                background: #f8f9fa;
                border-left: 4px solid #28a745;
                border-radius: 3px;
                white-space: pre-wrap;
                font-family: monospace;
            }}
            .stack-trace {{
                margin: 10px 0;
                padding: 10px;
                background: #f8f9fa;
                border-left: 4px solid #007bff;
                border-radius: 3px;
            }}
            .stack-trace-call {{
                margin: 5px 0;
                padding: 10px;
                background: #f8f9fa;
                border-left: 4px solid #17a2b8;
                border-radius: 3px;
            }}
            .stack-trace-result {{
                margin: 5px 0;
                padding: 10px;
                background: #f8f9fa;
                border-left: 4px solid #28a745;
                border-radius: 3px;
            }}
            .stack-trace-error {{
                margin: 5px 0;
                padding: 10px;
                background: #f8f9fa;
                border-left: 4px solid #dc3545;
                border-radius: 3px;
            }}
            .controls {{
                position: fixed;
                bottom: 20px;
                right: 20px;
                display: flex;
                gap: 10px;
                background: white;
                padding: 10px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            button {{
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                background: #007bff;
                color: white;
                cursor: pointer;
                font-size: 14px;
            }}
            button:hover {{
                background: #0056b3;
            }}
            .hidden {{
                display: none;
            }}
        </style>
    </head>
    <body>
        <div id="presentation"></div>
        <div class="controls">
            <button onclick="previousSlide()">Previous</button>
            <button onclick="nextSlide()">Next</button>
        </div>
        
        <script>
            const presentationData = {json.dumps(presentation_data)};
            let currentSlideIndex = 0;
            
            function displaySlide(index) {{
                const container = document.getElementById('presentation');
                const slide = presentationData.slides[index];
                
                container.innerHTML = `
                    <div class="slide">
                        ${{slide.title ? `<h2 class="slide-title">${{slide.title}}</h2>` : ''}}
                        ${{slide.description ? `<p class="slide-description">${{slide.description}}</p>` : ''}}
                        
                        <pre><code class="language-python">${{slide.code}}</code></pre>
                        
                        ${{Object.entries(slide.annotations)
                            .map(([line, text]) => `
                                <div class="annotation">
                                    <strong>Line ${{line}}:</strong> ${{text}}
                                </div>
                            `).join('')}}
                        
                        ${{slide.execution_output ? `
                            <div class="execution-output">
                                <strong>Output:</strong>
                                <pre>${{slide.execution_output}}</pre>
                            </div>
                        ` : ''}}
                        
                        ${{slide.stack_trace ? `
                            <div class="stack-trace">
                                <strong>Stack Trace for ${{slide.stack_trace.function_name}}:</strong>
                                <pre><code class="language-python">${{slide.stack_trace.source}}</code></pre>
                                
                                <div class="stack-trace-details">
                                    <h4>Function Calls:</h4>
                                    ${{slide.stack_trace.trace_info.calls.map(call => `
                                        <div class="stack-trace-call">
                                            <strong>Called from:</strong> ${{call.caller || 'main'}}
                                            <br>
                                            <strong>Line:</strong> ${{call.line}}
                                            <br>
                                            <strong>Arguments:</strong> ${{JSON.stringify(call.args, null, 2)}}
                                        </div>
                                    `).join('')}}
                                    
                                    ${{slide.stack_trace.trace_info.result !== undefined ? `
                                        <div class="stack-trace-result">
                                            <strong>Result:</strong> ${{slide.stack_trace.trace_info.result}}
                                        </div>
                                    ` : ''}}
                                    
                                    ${{slide.stack_trace.trace_info.error ? `
                                        <div class="stack-trace-error">
                                            <strong>Error:</strong>
                                            <pre>${{slide.stack_trace.trace_info.error}}</pre>
                                            <pre>${{slide.stack_trace.trace_info.traceback}}</pre>
                                        </div>
                                    ` : ''}}
                                    
                                    ${{slide.stack_trace.trace_info.output ? `
                                        <div class="stack-trace-result">
                                            <strong>Output:</strong>
                                            <pre>${{slide.stack_trace.trace_info.output}}</pre>
                                        </div>
                                    ` : ''}}
                                </div>
                            </div>
                        ` : ''}}
                        
                        ${{Object.entries(slide.visualizations)
                            .map(([name, data]) => `
                                <div class="visualization">
                                    <h3>${{name}}</h3>
                                    <pre>${{JSON.stringify(data, null, 2)}}</pre>
                                </div>
                            `).join('')}}
                    </div>
                `;
                
                // Apply syntax highlighting
                document.querySelectorAll('pre code').forEach((block) => {{
                    hljs.highlightBlock(block);
                }});
            }}
            
            function nextSlide() {{
                if (currentSlideIndex < presentationData.slides.length - 1) {{
                    currentSlideIndex++;
                    displaySlide(currentSlideIndex);
                }}
            }}
            
            function previousSlide() {{
                if (currentSlideIndex > 0) {{
                    currentSlideIndex--;
                    displaySlide(currentSlideIndex);
                }}
            }}
            
            // Initialize first slide
            displaySlide(0);
            
            // Handle keyboard navigation
            document.addEventListener('keydown', (e) => {{
                if (e.key === 'ArrowRight' || e.key === 'Space') {{
                    nextSlide();
                }} else if (e.key === 'ArrowLeft') {{
                    previousSlide();
                }}
            }});
        </script>
    </body>
    </html>
    """ 