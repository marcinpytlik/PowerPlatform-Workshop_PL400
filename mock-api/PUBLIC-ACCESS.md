# Mock API – publiczny dostęp dla zdalnego warsztatu

## Cel

Dokument opisuje najprostszy wariant udostępnienia lokalnego mock API zdalnym uczestnikom:

```text
Power Automate uczestnika
        |
        v
publiczny HTTPS
        |
        v
Cloudflare Tunnel
        |
        v
localhost:8080
        |
        v
Docker
        |
        v
vcm-mock-api
```

Uczestnik nie instaluje mock API ani Dockera. Otrzymuje tylko publiczny Base URL.

## 1. Wymagania na komputerze prowadzącego

- Docker Desktop albo Docker Engine,
- Git,
- PowerShell,
- `cloudflared`,
- dostęp wychodzący do Internetu.

## 2. Pobranie repozytorium

```powershell
git clone https://github.com/marcinpytlik/PowerPlatform-Workshop_PL400.git
cd PowerPlatform-Workshop_PL400
```

Jeżeli repozytorium jest już lokalnie:

```powershell
git pull
```

## 3. Budowa obrazu Docker

Z katalogu głównego repozytorium:

```powershell
docker build -t vcm-mock-api ./mock-api
```

Sprawdzenie obrazu:

```powershell
docker images vcm-mock-api
```

## 4. Uruchomienie kontenera

```powershell
docker run -d --name vcm-mock-api -p 8080:8080 vcm-mock-api
```

Sprawdzenie:

```powershell
docker ps
```

Logi:

```powershell
docker logs vcm-mock-api
```

## 5. Test lokalny

```powershell
Invoke-RestMethod http://localhost:8080/health
```

Dopiero po poprawnym lokalnym health checku należy wystawić API publicznie.

## 6. Instalacja cloudflared

Windows:

```powershell
winget install --id Cloudflare.cloudflared
```

Weryfikacja:

```powershell
cloudflared --version
```

## 7. Uruchomienie Quick Tunnel

W osobnym oknie PowerShell:

```powershell
cloudflared tunnel --url http://localhost:8080
```

Po chwili pojawi się komunikat podobny do:

```text
Your quick Tunnel has been created!
https://example-random-name.trycloudflare.com
```

Nie zamykaj tego procesu podczas zajęć.

## 8. Test publicznego endpointu

```powershell
$ApiBaseUrl = "https://example-random-name.trycloudflare.com"

Invoke-RestMethod "$ApiBaseUrl/health"
```

Jeżeli health check odpowiada poprawnie, endpoint jest dostępny z Internetu.

## 9. Test POST /api/contracts

```powershell
$ApiBaseUrl = "https://example-random-name.trycloudflare.com"

$body = @{
    contractNumber = "VCM/LAB04/201"
    supplierCode   = "SUP-001"
    amount         = 50000
    currency       = "PLN"
    correlationId  = "demo-001"
} | ConvertTo-Json

Invoke-RestMethod `
    -Method Post `
    -Uri "$ApiBaseUrl/api/contracts" `
    -ContentType "application/json" `
    -Body $body
```

Oczekiwany rezultat dla numeru zawierającego `201`: HTTP 201.

## 10. Informacja przekazywana uczestnikom

Prowadzący przekazuje tylko:

```text
VCM Mock API

Base URL:
https://example-random-name.trycloudflare.com

Health:
GET {BASE_URL}/health

Contracts:
POST {BASE_URL}/api/contracts
```

W Power Automate uczestnik używa:

```text
Method: POST
URI: https://example-random-name.trycloudflare.com/api/contracts
Content-Type: application/json
```

Przykładowe body:

```json
{
  "contractNumber": "VCM/LAB04/201",
  "supplierCode": "SUP-001",
  "amount": 50000,
  "currency": "PLN",
  "correlationId": "student-01-demo"
}
```

## 11. Scenariusze błędów

Mock API rozpoznaje tryb między innymi na podstawie numeru umowy:

```text
VCM/LAB04/201      -> 201
VCM/LAB04/409      -> 409
VCM/LAB04/429      -> 429
VCM/LAB04/500      -> 500
VCM/LAB04/SLOW     -> timeout
VCM/LAB04/TIMEOUT  -> timeout
```

Dzięki temu uczestnicy nie muszą zmieniać konfiguracji API ani korzystać ze wspólnego globalnego przełącznika.

## 12. Restart i cleanup

Zatrzymanie kontenera:

```powershell
docker stop vcm-mock-api
```

Usunięcie:

```powershell
docker rm vcm-mock-api
```

Ponowne uruchomienie:

```powershell
docker run -d --name vcm-mock-api -p 8080:8080 vcm-mock-api
```

Wyczyszczenie pamięci mock API:

```powershell
Invoke-RestMethod -Method Delete "$ApiBaseUrl/api/contracts"
```

## 13. Quick Tunnel a warsztat wielodniowy

Quick Tunnel jest wygodny, ale jego URL jest tymczasowy.

Jeżeli proces `cloudflared` zostanie zatrzymany:

- bieżący URL przestaje działać,
- po ponownym uruchomieniu może powstać nowy URL,
- trzeba wtedy zaktualizować `VCM_API_BASE_URL` i przekazać nowy adres uczestnikom.

Na warsztat wielodniowy lub cykliczny lepiej użyć:

- Cloudflare Named Tunnel z własną domeną,
- Azure Container Apps,
- Azure App Service,
- innego stałego hostingu HTTPS.

## 14. Checklista prowadzącego

Przed rozpoczęciem LAB 04:

- [ ] kontener `vcm-mock-api` działa,
- [ ] `http://localhost:8080/health` odpowiada,
- [ ] `cloudflared` działa,
- [ ] publiczny `/health` odpowiada,
- [ ] testowy POST zwraca 201,
- [ ] URL został przekazany uczestnikom,
- [ ] `VCM_API_BASE_URL` wskazuje publiczny adres,
- [ ] okno/proces `cloudflared` pozostaje uruchomione.
