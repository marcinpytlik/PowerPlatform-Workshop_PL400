#!/usr/bin/env python3
"""Start mock API on an ephemeral port and verify workshop modes."""

from __future__ import annotations

import json
import sys
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import server as mock  # noqa: E402


def request(method: str, url: str, body: dict | None = None, headers: dict | None = None):
    data = None if body is None else json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    for key, value in (headers or {}).items():
        req.add_header(key, value)
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            payload = json.loads(response.read().decode("utf-8"))
            return response.status, payload, dict(response.headers)
    except urllib.error.HTTPError as exc:
        payload = json.loads(exc.read().decode("utf-8"))
        return exc.code, payload, dict(exc.headers)


def expect(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    httpd = mock.create_server("127.0.0.1", 0)
    port = httpd.server_address[1]
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    time.sleep(0.1)
    base = f"http://127.0.0.1:{port}"

    try:
        status, payload, _ = request("GET", f"{base}/health")
        expect(status == 200, f"health status {status}")
        expect(payload["status"] == "ok", "health payload")

        created = {
            "contractNumber": "VCM/TEST/201",
            "supplierCode": "SUP-001",
            "amount": 50000,
            "currency": "PLN",
            "correlationId": "corr-201",
        }
        status, payload, _ = request("POST", f"{base}/api/contracts", created)
        expect(status == 201, f"success status {status}")
        expect(payload["id"].startswith("ERP-"), payload)
        expect(payload["correlationId"] == "corr-201", payload)
        external_id = payload["id"]

        status, payload, _ = request("POST", f"{base}/api/contracts", created)
        expect(status == 409, f"duplicate status {status}")
        expect(payload["code"] == "CONTRACT_ALREADY_EXISTS", payload)
        expect(payload["externalId"] == external_id, payload)

        status, payload, _ = request(
            "POST",
            f"{base}/api/contracts",
            {
                "contractNumber": "VCM/TEST/409-CASE",
                "supplierCode": "SUP-002",
                "amount": 10,
                "currency": "EUR",
            },
        )
        expect(status == 409, f"suffix 409 -> {status}")
        expect(payload["code"] == "CONTRACT_ALREADY_EXISTS", payload)

        status, payload, headers = request(
            "POST",
            f"{base}/api/contracts",
            {
                "contractNumber": "VCM/TEST/OK-1",
                "supplierCode": "SUP-002",
                "amount": 10,
                "currency": "EUR",
            },
            headers={"x-mock-mode": "429"},
        )
        expect(status == 429, f"header 429 -> {status}")
        expect(payload["code"] == "TOO_MANY_REQUESTS", payload)
        expect(headers.get("Retry-After") == "10", headers)

        status, payload, _ = request(
            "POST",
            f"{base}/api/contracts?mode=500",
            {
                "contractNumber": "VCM/TEST/OK-2",
                "supplierCode": "SUP-003",
                "amount": 20,
                "currency": "PLN",
            },
        )
        expect(status == 500, f"query 500 -> {status}")
        expect(payload["code"] == "INTERNAL_ERROR", payload)

        status, payload, _ = request(
            "POST",
            f"{base}/api/contracts",
            {"contractNumber": "VCM/X", "amount": 1, "currency": "PLN"},
        )
        expect(status == 400, f"missing supplierCode -> {status}")
        expect("supplierCode" in payload.get("fields", []), payload)

        status, payload, _ = request(
            "PUT",
            f"{base}/admin/mode",
            {"mode": "error"},
        )
        expect(status == 200 and payload["mode"] == "error", payload)
        status, payload, _ = request(
            "POST",
            f"{base}/api/contracts",
            {
                "contractNumber": "VCM/TEST/GLOBAL",
                "supplierCode": "SUP-001",
                "amount": 1,
                "currency": "PLN",
            },
        )
        expect(status == 500, f"global error -> {status}")

        status, payload, _ = request("DELETE", f"{base}/api/contracts")
        expect(status == 200, payload)
        status, payload, _ = request("GET", f"{base}/api/contracts")
        expect(payload["value"] == [], payload)

        print("mock API tests passed")
    finally:
        httpd.shutdown()
        httpd.server_close()


if __name__ == "__main__":
    main()
