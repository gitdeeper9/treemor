"""
TREEMOR Dashboard - Web interface for monitoring.
Pure Python implementation - NO NUMPY
"""

import sys
import json
from typing import Dict, Optional


class Dashboard:
    """
    Simple dashboard for TREEMOR monitoring.
    
    Note: Full Dash application requires dash/plotly.
    This is a placeholder for the dashboard functionality.
    """
    
    def __init__(self):
        self.title = "TREEMOR - Bio-Seismic Sensing Dashboard"
        self.version = "1.0.0"
    
    def run(self, host: str = "0.0.0.0", port: int = 8050, debug: bool = False):
        """
        Run the dashboard.
        
        Args:
            host: Host to bind to
            port: Port to listen on
            debug: Enable debug mode
        """
        print("=" * 60)
        print(f"🌲 {self.title}")
        print(f"📡 Version: {self.version}")
        print(f"🔗 DOI: {__import__('treomor').__doi__}")
        print("=" * 60)
        print()
        print("⚠️  Full dashboard requires dash and plotly.")
        print("   Install with: pip install treomor[dash]")
        print()
        print(f"📊 To access the full dashboard, install dependencies and run:")
        print(f"   $ pip install dash plotly")
        print(f"   $ python -c 'from treomor.dashboard.app import Dashboard; Dashboard().run()'")
        print()
        print("💡 Current status: Placeholder mode")
        print()
        
        # Simple HTTP server for basic status
        import http.server
        import socketserver
        
        class Handler(http.server.SimpleHTTPRequestHandler):
            def do_GET(self):
                if self.path == '/':
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    
                    html = f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>TREEMOR Dashboard</title>
                        <style>
                            body {{ font-family: monospace; margin: 40px; background: #1a1a2e; color: #eee; }}
                            h1 {{ color: #4caf50; }}
                            .container {{ max-width: 800px; margin: auto; }}
                            .status {{ background: #16213e; padding: 20px; border-radius: 8px; }}
                            .green {{ color: #4caf50; }}
                            .warning {{ color: #ff9800; }}
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <h1>🌲 TREEMOR Dashboard</h1>
                            <p><em>Bio-Seismic Sensing & Planetary Infrasound Resonance</em></p>
                            <hr>
                            <div class="status">
                                <h2>📡 System Status</h2>
                                <p><span class="green">●</span> Dashboard: <strong>Active</strong> (Placeholder Mode)</p>
                                <p>Version: {self.version}</p>
                                <p>DOI: {__import__('treomor').__doi__}</p>
                                <p><span class="warning">⚠️</span> Full functionality requires dash/plotly</p>
                            </div>
                            <hr>
                            <p>📖 <a href="https://treomor.netlify.app" style="color: #4caf50;">Documentation</a> | 
                               🔗 <a href="https://doi.org/{__import__('treomor').__doi__}" style="color: #4caf50;">DOI</a></p>
                            <p><em>When forests become Earth's sentinels, conservation becomes infrastructure.</em></p>
                        </div>
                    </body>
                    </html>
                    """
                    self.wfile.write(html.encode())
                else:
                    self.send_response(404)
                    self.end_headers()
        
        with socketserver.TCPServer((host, port), Handler) as httpd:
            print(f"🌐 Dashboard running at http://{host}:{port}")
            print("Press Ctrl+C to stop")
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\n👋 Shutting down...")
                httpd.shutdown()


def run():
    """Entry point for dashboard."""
    dashboard = Dashboard()
    dashboard.run()


if __name__ == "__main__":
    run()
