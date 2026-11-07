#!/usr/bin/env python3
"""Serve the Harvard Pops website locally.

Usage:  python3 run.py [port]
Then open http://localhost:8000 (or the port you chose).

The site itself is plain static HTML/CSS/JS, so the exact same files
also work when published through GitHub Pages.
"""

import http.server
import os
import socketserver
import sys
import webbrowser

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
ROOT = os.path.dirname(os.path.abspath(__file__))


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def end_headers(self):
        # No caching while developing locally.
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True


def main():
    with Server(("", PORT), Handler) as httpd:
        url = f"http://localhost:{PORT}/"
        print(f"Serving Harvard Pops website at {url}")
        print("Press Ctrl+C to stop.")
        try:
            webbrowser.open(url)
        except Exception:
            pass
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")


if __name__ == "__main__":
    main()
