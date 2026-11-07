#!/usr/bin/env python3
"""Serve the Harvard Pops website locally.

Usage:  python3 run.py [port]
Then open http://localhost:8000 (or the port you chose).

Uses Flask when available, falling back to the standard library server.
The site itself is plain static HTML/CSS/JS, so the exact same files
also work when published through GitHub Pages.
"""

import os
import sys
import webbrowser

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
ROOT = os.path.dirname(os.path.abspath(__file__))


def run_flask():
    from flask import Flask, send_from_directory

    app = Flask(__name__, static_folder=None)

    @app.route("/")
    @app.route("/<path:path>")
    def serve(path="index.html"):
        full = os.path.join(ROOT, path)
        if os.path.isdir(full):
            path = os.path.join(path, "index.html")
        resp = send_from_directory(ROOT, path)
        resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        return resp

    print(f"Serving Harvard Pops website (Flask) at http://localhost:{PORT}/")
    print("Press Ctrl+C to stop.")
    app.run(host="0.0.0.0", port=PORT, debug=False)


def run_stdlib():
    import http.server
    import socketserver

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=ROOT, **kwargs)

        def end_headers(self):
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            super().end_headers()

    class Server(socketserver.ThreadingTCPServer):
        allow_reuse_address = True

    with Server(("", PORT), Handler) as httpd:
        print(f"Serving Harvard Pops website at http://localhost:{PORT}/")
        print("(Install Flask for the Flask-powered server: pip install flask)")
        print("Press Ctrl+C to stop.")
        httpd.serve_forever()


def main():
    try:
        webbrowser.open(f"http://localhost:{PORT}/")
    except Exception:
        pass
    try:
        run_flask()
    except ImportError:
        try:
            run_stdlib()
        except KeyboardInterrupt:
            print("\nStopped.")
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
