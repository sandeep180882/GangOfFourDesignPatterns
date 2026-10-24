"""Tiny browser UI (standard library only). Run: `python -m ui.server [port]`."""

from __future__ import annotations

import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from catalog import discover, find

INDEX = Path(__file__).with_name("index.html")


class Handler(BaseHTTPRequestHandler):
    def _send(self, body: bytes, content_type: str, status: int = 200) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _json(self, payload: object, status: int = 200) -> None:
        self._send(json.dumps(payload).encode(), "application/json", status)

    def do_GET(self) -> None:  # noqa: N802 (http.server API)
        url = urlparse(self.path)
        if url.path == "/":
            self._send(INDEX.read_bytes(), "text/html; charset=utf-8")
        elif url.path == "/api/demos":
            self._json([{"id": d.id, "group": d.group, "name": d.name} for d in discover()])
        elif url.path == "/api/run":
            demo = find(parse_qs(url.query).get("id", [""])[0])
            if demo is None:
                self._json({"error": "unknown demo"}, 404)
            else:
                self._json({"output": demo.run(), "readme": demo.readme_text()})
        else:
            self._send(b"Not found", "text/plain", 404)

    def log_message(self, format: str, *args: object) -> None:  # keep console quiet
        pass


def main() -> None:
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"Design Patterns UI running at http://127.0.0.1:{port}  (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
