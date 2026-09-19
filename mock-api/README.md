# Mock API – Vendor Contract Management

Lekki serwer HTTP bez zależności zewnętrznych. Służy do LAB 04, 09, 11 i 13.

## Uruchomienie

```bash
cd mock-api
python3 server.py
```

Domyślny adres: `http://localhost:8080`.

| Zmienna | Domyślnie | Znaczenie |
|---|---|---|
| `PORT` / `VCM_MOCK_PORT` | `8080` | port |
| `VCM_MOCK_HOST` | `0.0.0.0` | interfejs |
| `VCM_MOCK_DEFAULT_MODE` | `success` | tryb, gdy nie podano innego |
| `VCM_MOCK_TIMEOUT_SECONDS` | `35` | opóźnienie trybu `timeout` |
| `VCM_MOCK_RETRY_AFTER` | `10` | wartość nagłówka `Retry-After` |

Kontener:

```bash
docker build -t vcm-mock-api ./mock-api
docker run --rm -p 8080:8080 vcm-mock-api
```

Na sali wystaw publiczny HTTPS (ngrok, cloudflared, Container Apps). Ten URL trafia do `VCM_API_BASE_URL`.

## Kontrakt

`POST /api/contracts`

```json
{
  "contractNumber": "VCM/2026/001",
  "supplierCode": "SUP-001",
  "amount": 50000,
  "currency": "PLN",
  "correlationId": "7c2e..."
}
```

Wymagane: `contractNumber`, `supplierCode`, `amount`, `currency`.
Opcjonalnie nagłówek `x-correlation-id`.

## Tryby odpowiedzi

Kolejność rozstrzygania:

1. nagłówek `x-mock-mode`,
2. query `?mode=`,
3. numer umowy zawierający `201`, `409`, `429`, `500`, `SLOW` albo `TIMEOUT`,
4. tryb globalny `/admin/mode`,
5. `VCM_MOCK_DEFAULT_MODE`.

| Tryb | HTTP | Ciało / nagłówki |
|---|---:|---|
| `success` / `201` | 201 | `id`, `status=created`, `correlationId` |
| `conflict` / `409` | 409 | `CONTRACT_ALREADY_EXISTS`, `externalId` |
| `throttle` / `429` | 429 | `Retry-After`, `TOO_MANY_REQUESTS` |
| `error` / `500` | 500 | `INTERNAL_ERROR` |
| `timeout` | czeka, potem 500 | do testu timeoutu akcji HTTP |

Ponowny `POST` tego samego `contractNumber` w trybie `success` zwraca **409**. To jest celowe – ćwiczy idempotencję.

## Przykłady dla sali

Happy path:

```bash
curl -i -X POST "$API/api/contracts" \
  -H 'Content-Type: application/json' \
  -H 'x-correlation-id: demo-1' \
  -d '{"contractNumber":"VCM/2026/001","supplierCode":"SUP-001","amount":50000,"currency":"PLN","correlationId":"demo-1"}'
```

Macierz LAB 04 bez zmiany trybu globalnego:

```text
VCM/LAB04/201   -> 201
VCM/LAB04/409   -> 409
VCM/LAB04/429   -> 429
VCM/LAB04/500   -> 500
VCM/LAB04/SLOW  -> timeout
```

Albo jeden numer i nagłówek:

```bash
curl -i -X POST "$API/api/contracts" \
  -H 'Content-Type: application/json' \
  -H 'x-mock-mode: 429' \
  -d '{"contractNumber":"VCM/2026/002","supplierCode":"SUP-002","amount":150000,"currency":"EUR","correlationId":"demo-2"}'
```

Tryb globalny dla całego labu:

```bash
curl -s -X PUT "$API/admin/mode" \
  -H 'Content-Type: application/json' \
  -d '{"mode":"error"}'
```

Reset pamięci przed kolejną grupą:

```bash
curl -s -X DELETE "$API/api/contracts"
```

## Inne ścieżki

| Metoda | Ścieżka | Opis |
|---|---|---|
| GET | `/health` | status serwisu |
| GET | `/api/contracts` | zarejestrowane umowy |
| DELETE | `/api/contracts` | czyści magazyn |
| GET | `/admin/mode` | bieżący tryb globalny |
| PUT | `/admin/mode` | ustawia tryb globalny |

## Testy

```bash
python3 mock-api/test_server.py
```

Pełny kontrakt: [`../11-api-integration/openapi.yaml`](../11-api-integration/openapi.yaml).
