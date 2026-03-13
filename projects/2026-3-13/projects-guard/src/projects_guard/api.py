from __future__ import annotations

import json
from dataclasses import asdict
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from .guard import ProtectedAgent, load_cases, simulate_cases


class GuardAPIHandler(BaseHTTPRequestHandler):
    agent = ProtectedAgent(api_key="sk-live-EXAMPLE-123456")

    def do_GET(self) -> None:  # noqa: N802
        if self.path != "/health":
            self._send_json({"error": "not found"}, status=HTTPStatus.NOT_FOUND)
            return
        self._send_json({"status": "ok"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path == "/guard":
            self._handle_guard()
            return
        if self.path == "/evaluate":
            self._handle_evaluate()
            return
        self._send_json({"error": "not found"}, status=HTTPStatus.NOT_FOUND)

    def log_message(self, format: str, *args: Any) -> None:
        return

    def _handle_guard(self) -> None:
        payload = self._read_json()
        if payload is None:
            return
        prompt = str(payload.get("prompt", ""))
        external_text = str(payload.get("external_text", ""))
        api_key = payload.get("api_key")
        if api_key is not None:
            self.agent = ProtectedAgent(api_key=str(api_key))
        decision = self.agent.handle(prompt, external_text)
        self._send_json(asdict(decision))

    def _handle_evaluate(self) -> None:
        payload = self._read_json(allow_empty=True)
        if payload is None:
            return
        api_key = str(payload.get("api_key", "sk-live-EXAMPLE-123456"))
        metrics = simulate_cases(load_cases(), api_key=api_key)
        self._send_json(metrics)

    def _read_json(self, allow_empty: bool = False) -> dict[str, Any] | None:
        content_length = int(self.headers.get("Content-Length", "0"))
        if content_length == 0 and allow_empty:
            return {}
        if content_length == 0:
            self._send_json({"error": "empty body"}, status=HTTPStatus.BAD_REQUEST)
            return None
        raw = self.rfile.read(content_length)
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            self._send_json({"error": "invalid json"}, status=HTTPStatus.BAD_REQUEST)
            return None
        if not isinstance(payload, dict):
            self._send_json({"error": "json body must be an object"}, status=HTTPStatus.BAD_REQUEST)
            return None
        return payload

    def _send_json(self, payload: dict[str, Any], status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def run_server(host: str = "127.0.0.1", port: int = 8000) -> None:
    server = ThreadingHTTPServer((host, port), GuardAPIHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
