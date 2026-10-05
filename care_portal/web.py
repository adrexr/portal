"""Dependency-free server for a non-clinical demo portal."""

from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from api.portal import access_portal_payload, acknowledge_payload


class PortalHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if urlparse(self.path).path == "/":
            self._send(HTTPStatus.OK, "text/html; charset=utf-8", (Path(__file__).resolve().parent.parent / "index.html").read_text(encoding="utf-8"))
            return
        self._send(HTTPStatus.NOT_FOUND, "text/plain; charset=utf-8", "Ruta no encontrada")

    def do_POST(self) -> None:
        route = urlparse(self.path).path
        if route not in {"/api/portal/access", "/api/portal/follow-up"}:
            self._send(HTTPStatus.NOT_FOUND, "text/plain; charset=utf-8", "Ruta no encontrada")
            return
        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            if content_length <= 0 or content_length > 5_000:
                raise ValueError("Solicitud inválida.")
            data = json.loads(self.rfile.read(content_length).decode("utf-8"))
            if not isinstance(data, dict):
                raise ValueError("Solicitud inválida.")
            payload = access_portal_payload(data) if route.endswith("access") else acknowledge_payload(data)
            self._send_json(HTTPStatus.OK, payload)
        except (ValueError, json.JSONDecodeError) as error:
            self._send_json(HTTPStatus.BAD_REQUEST, {"success": False, "error": str(error)})

    def _send_json(self, status: HTTPStatus, payload: dict) -> None:
        self._send(status, "application/json; charset=utf-8", json.dumps(payload, ensure_ascii=False))

    def _send(self, status: HTTPStatus, content_type: str, body: str) -> None:
        encoded = body.encode("utf-8")
        self.send_response(status); self.send_header("Content-Type", content_type); self.send_header("Content-Length", str(len(encoded))); self.end_headers(); self.wfile.write(encoded)

    def log_message(self, _format: str, *_args) -> None:
        return


def run_server(port: int = 8002) -> None:
    server = ThreadingHTTPServer(("127.0.0.1", port), PortalHandler)
    print(f"Portal de seguimiento disponible en http://127.0.0.1:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
