#!/usr/bin/env python3
"""Vendor Contract Management – mock API for the Advanced Workshop.

Modes: success (201), conflict (409), throttle (429), error (500), timeout.
"""

from __future__ import annotations

import json
import os
import re
import threading
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

DEFAULT_HOST = os.environ.get("VCM_MOCK_HOST", "0.0.0.0")
DEFAULT_PORT = int(os.environ.get("PORT") or os.environ.get("VCM_MOCK_PORT") or "8080")
DEFAULT_MODE = os.environ.get("VCM_MOCK_DEFAULT_MODE", "success").strip().lower()
TIMEOUT_SECONDS = float(os.environ.get("VCM_MOCK_TIMEOUT_SECONDS", "35"))
RETRY_AFTER_SECONDS = os.environ.get("VCM_MOCK_RETRY_AFTER", "10")

VALID_MODES = {"success", "conflict", "throttle", "error", "timeout", "201", "409", "429", "500"}

MODE_ALIASES = {
    "201": "success",
    "409": "conflict",
    "429": "throttle",
    "500": "error",
    "success": "success",
    "conflict": "conflict",
    "throttle": "throttle",
    "error": "error",
    "timeout": "timeout",
    "slow": "timeout",
}

STORE_LOCK = threading.Lock()
STORE: dict[str, dict] = {}
STATE = {
    "global_mode": DEFAULT_MODE if DEFAULT_MODE in MODE_ALIASES else "success",
    "started_at": time.time(),
}


def normalize_mode(value: str | None) -> str | None:
    if not value:
        return None
    key = value.strip().lower()
    return MODE_ALIASES.get(key)


def mode_from_contract_number(contract_number: str) -> str | None:
    if not contract_number:
        return None
    token = contract_number.upper()
    if re.search(r"(TIMEOUT|SLOW)", token):
        return "timeout"
    match = re.search(r"(409|429|500|201)", token)
    if not match:
        return None
    return normalize_mode(match.group(1))


def next_external_id() -> str:
    return f"ERP-{str(uuid.uuid4().int)[-5:]}"


def json_bytes(payload: dict, status: int) -> tuple[int, bytes]:
    return status, json.dumps(payload, ensure_ascii=False).encode("utf-8")


class MockHandler(BaseHTTPRequestHandler):
    server_version = "VCMMockAPI/1.0"

    def log_message(self, fmt: str, *args) -> None:
        correlation = self.headers.get("x-correlation-id", "-")
        print(f"{self.address_string()} {correlation} {fmt % args}")

    def _send(self, status: int, payload: dict, extra_headers: dict | None = None) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        if extra_headers:
            for key, value in extra_headers.items():
                self.send_header(key, value)
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self) -> dict:
        length = int(self.headers.get("Content-Length") or "0")
        raw = self.rfile.read(length) if length else b""
        if not raw:
            return {}
        return json.loads(raw.decode("utf-8"))

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path in {"/", "/health"}:
            self._send(
                200,
                {
                    "status": "ok",
                    "service": "vcm-mock-api",
                    "defaultMode": STATE["global_mode"],
                    "contracts": len(STORE),
                },
            )
            return
        if parsed.path == "/admin/mode":
            self._send(200, {"mode": STATE["global_mode"]})
            return
        if parsed.path == "/api/contracts":
            with STORE_LOCK:
                items = list(STORE.values())
            self._send(200, {"value": items})
            return
        self._send(404, {"code": "NOT_FOUND", "message": "Unknown path"})

    def do_DELETE(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path != "/api/contracts":
            self._send(404, {"code": "NOT_FOUND", "message": "Unknown path"})
            return
        with STORE_LOCK:
            STORE.clear()
        self._send(200, {"status": "cleared"})

    def do_PUT(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path != "/admin/mode":
            self._send(404, {"code": "NOT_FOUND", "message": "Unknown path"})
            return
        try:
            body = self._read_json()
        except json.JSONDecodeError:
            self._send(400, {"code": "INVALID_JSON", "message": "Body must be JSON"})
            return
        mode = normalize_mode(str(body.get("mode", "")))
        if mode is None:
            self._send(
                400,
                {
                    "code": "INVALID_MODE",
                    "message": "Use success, conflict, throttle, error, timeout",
                },
            )
            return
        STATE["global_mode"] = mode
        self._send(200, {"mode": mode})

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path != "/api/contracts":
            self._send(404, {"code": "NOT_FOUND", "message": "Unknown path"})
            return

        try:
            body = self._read_json()
        except json.JSONDecodeError:
            self._send(400, {"code": "INVALID_JSON", "message": "Body must be JSON"})
            return

        required = ["contractNumber", "supplierCode", "amount", "currency"]
        missing = [field for field in required if body.get(field) in (None, "")]
        if missing:
            self._send(
                400,
                {
                    "code": "INVALID_REQUEST",
                    "message": "Missing required fields",
                    "fields": missing,
                },
            )
            return

        try:
            amount = float(body["amount"])
        except (TypeError, ValueError):
            self._send(
                400,
                {
                    "code": "INVALID_REQUEST",
                    "message": "amount must be a number",
                },
            )
            return

        query = parse_qs(parsed.query)
        mode = (
            normalize_mode(self.headers.get("x-mock-mode"))
            or normalize_mode((query.get("mode") or [None])[0])
            or mode_from_contract_number(str(body.get("contractNumber", "")))
            or STATE["global_mode"]
        )

        contract_number = str(body["contractNumber"]).strip()
        correlation_id = str(
            body.get("correlationId") or self.headers.get("x-correlation-id") or ""
        )

        if mode == "timeout":
            time.sleep(TIMEOUT_SECONDS)
            # After the wait the action in Power Automate should already time out.
            # Still return 500 so a client without timeout sees a technical error.
            mode = "error"

        if mode == "throttle":
            self._send(
                429,
                {
                    "code": "TOO_MANY_REQUESTS",
                    "message": "External system is throttling requests",
                    "correlationId": correlation_id,
                },
                extra_headers={"Retry-After": RETRY_AFTER_SECONDS},
            )
            return

        if mode == "error":
            self._send(
                500,
                {
                    "code": "INTERNAL_ERROR",
                    "message": "External system failed while registering the contract",
                    "correlationId": correlation_id,
                },
            )
            return

        with STORE_LOCK:
            existing = STORE.get(contract_number)
            if mode == "conflict" or existing is not None:
                external_id = existing["id"] if existing else "ERP-9999"
                self._send(
                    409,
                    {
                        "code": "CONTRACT_ALREADY_EXISTS",
                        "message": "Contract already exists in external system",
                        "externalId": external_id,
                        "correlationId": correlation_id,
                    },
                )
                return

            record = {
                "id": next_external_id(),
                "status": "created",
                "contractNumber": contract_number,
                "supplierCode": str(body["supplierCode"]),
                "amount": amount,
                "currency": str(body["currency"]),
                "correlationId": correlation_id,
            }
            STORE[contract_number] = record

        self._send(201, record)


def create_server(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> ThreadingHTTPServer:
    return ThreadingHTTPServer((host, port), MockHandler)


def main() -> None:
    server = create_server()
    print(f"VCM mock API listening on http://{DEFAULT_HOST}:{DEFAULT_PORT}")
    print(f"Default mode: {STATE['global_mode']}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Stopping mock API")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
