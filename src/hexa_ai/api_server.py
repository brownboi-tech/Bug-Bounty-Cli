from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from .runner import run_scan
from .settings import get_settings


class HexaAIHandler(BaseHTTPRequestHandler):
    def _send_json(self, code: int, payload: dict) -> None:
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode('utf-8'))

    def do_GET(self):  # noqa: N802
        if self.path == '/health':
            self._send_json(200, {'status': 'ok'})
            return
        self._send_json(404, {'error': 'not found'})

    def do_POST(self):  # noqa: N802
        if self.path != '/scan':
            self._send_json(404, {'error': 'not found'})
            return

        length = int(self.headers.get('Content-Length', '0'))
        body = self.rfile.read(length)
        payload = json.loads(body or b'{}')

        target = payload.get('target')
        if not target:
            self._send_json(400, {'error': 'target is required'})
            return

        fast = bool(payload.get('fast', False))
        settings = get_settings()
        run_scan(target, fast, settings.scan_output_dir)
        self._send_json(202, {'status': 'accepted', 'target': target, 'fast': fast})


def main() -> None:
    settings = get_settings()
    server = HTTPServer((settings.api_host, settings.api_port), HexaAIHandler)
    print(f'[*] Hexa AI API listening on {settings.api_host}:{settings.api_port}')
    server.serve_forever()


if __name__ == '__main__':
    main()
