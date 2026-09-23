# LAB 04 – HTTP, Settings, Run after i błędy integracji

## Cel laboratorium

Rozszerzyć proces o integrację HTTP i nauczyć się świadomie konfigurować zachowanie akcji w Power Automate.

Laboratorium obejmuje:

- HTTP POST,
- statusy 2xx/4xx/5xx,
- 409 Conflict,
- 429 Too Many Requests,
- retry policy,
- timeout,
- Run after,
- Secure inputs/outputs,
- Tracking,
- correlation ID.

## Czas

90 minut. W agendzie 3-dniowej: **75 min** (wariant na sali poniżej).

## Wymagania

- ukończony LAB 03,
- uruchomione [mock API](../mock-api/README.md) z publicznym HTTPS,
- `VCM_API_BASE_URL` albo tymczasowy URL rozdany przez prowadzącego,
- możliwość użycia akcji HTTP w środowisku szkoleniowym.

> Akcja HTTP może wymagać odpowiedniej licencji. Gdy HTTP albo DLP blokują LAB, użyj [PLAN-B](../trainer/PLAN-B.md).

## Wariant na sali (75 min)

Pełna macierz z zadania 11 ma 90 minut. W agendzie 3-dniowej zrób testy A, C, D/E i F. Test B (400) i timeout zostaw jako demo prowadzącego. 

---

# Docelowy fragment procesu

```text
Approved Contract
      |
      v
Compose Request
      |
      v
HTTP POST /api/contracts
      |
      +-- 201 -> save ExternalSystemId
      |
      +-- 409 -> business conflict
      |
      +-- 429 -> retry/throttling
      |
      +-- 5xx -> technical error
```

---

# Zadanie 1 – Ustawienie stanu integracji

Przed zbudowaniem requestu zaktualizuj umowę:

```text
Status = Integration Pending
```

Ten status oznacza, że proces biznesowej akceptacji zakończył się poprawnie, ale synchronizacja z systemem zewnętrznym jeszcze trwa. Dopiero odpowiedź 201 kończy proces statusem `Integrated`, a błąd techniczny prowadzi później do `Integration Error`.

---

# Zadanie 2 – Przygotowanie requestu

Dodaj Scope `External Integration` po końcowym Approved.

Dodaj Compose `Compose - API Request`. Kontrakt API używa **`supplierCode`**, nie nazwy wyświetlanej dostawcy.

```json
{
  "contractNumber": "<ContractNumber / Title>",
  "supplierCode": "<SupplierCode z Get Supplier>",
  "amount": "<amount>",
  "currency": "<currency>",
  "correlationId": "<correlation id>"
}
```

W designerze nie wklejaj literalnie placeholderów `<...>` – wybierz dynamic content z flow. `supplierCode` weź z listy/tabeli dostawcy, nie z Lookup display name.

Przykład zgodny z [`../04-api-integration/openapi.yaml`](../04-api-integration/openapi.yaml):

```json
{
  "contractNumber": "VCM/2026/001",
  "supplierCode": "SUP-001",
  "amount": 50000,
  "currency": "PLN",
  "correlationId": "7c2e9b1a-demo"
}
```

## Cel

Request ma być widoczny jako osobny krok przed HTTP. Ułatwia to diagnostykę i pozwala odróżnić błąd budowy payloadu od błędu wywołania API.

---

# Zadanie 3 – Akcja HTTP

Dodaj akcję `HTTP`.

Ustaw:

```text
Method: POST
URI: <VCM_API_BASE_URL>/api/contracts
```

Na tym etapie URL może być jeszcze wpisany ręcznie. W LAB 12 zastąpimy go Environment Variable. Nie używaj `localhost` – Power Automate nie zobaczy laptopa uczestnika.

Headers:

```text
Content-Type : application/json
x-correlation-id : <CorrelationId>
```

Body: output `Compose - API Request`.

Zmień nazwę akcji na:

```text
HTTP - Create Contract
```

---

# Zadanie 4 – Settings akcji

Zaznacz `HTTP - Create Contract`, następnie otwórz kartę **Settings / Ustawienia**.

Przejrzyj sekcje dostępne w bieżącym designerze. Microsoft w nowym designerze udostępnia w Settings m.in. ustawienia timeout, network retry policy, uruchamiania, security input/output i tracking.

## Timeout

Ustaw demonstracyjnie timeout, np.:

```text
PT30S
```

Omów format ISO 8601 Duration.

> W produkcji wartość dobieramy do kontraktu API. Nie ustawiamy losowo krótkiego timeout tylko dlatego, że „flow ma działać szybko”.

## Retry policy

Porównaj:

- Default,
- None,
- Fixed interval,
- Exponential interval – jeśli opcja jest dostępna dla danej akcji.

Na pierwszy test ustaw `None`.

## Secure inputs / Secure outputs

1. Zlokalizuj ustawienia bezpieczeństwa.
2. Włącz `Secure inputs` lub `Secure outputs` tylko demonstracyjnie.
3. Zapisz flow.
4. Wykonaj test.
5. Sprawdź Run History – zabezpieczona zawartość nie powinna być ujawniona w historii.
6. Wyłącz Secure dla dalszej części LAB, aby móc analizować payload.

Omów kompromis:

```text
security vs diagnosability
```

## Tracking

Jeśli dostępne jest Tracking / Tracked properties:

Dodaj do tracked properties np.:

```text
ContractNumber
ContractId
Status
```

Wartości wybierz z triggera albo z inputs/outputs **tej samej akcji**.

> Ważne ograniczenie: tracked properties akcji nie mogą odwoływać się dowolnie do outputów wcześniejszych akcji. W praktyce odwołanie typu `outputs('Compose_-_Correlation_ID')` użyte bezpośrednio w Tracking akcji HTTP może zakończyć zapis flow błędem `InvalidTemplate`. Tracked properties mogą korzystać z własnych inputs/outputs akcji, trigger inputs/outputs oraz parameters.
>
> Dlatego `CorrelationId` wygenerowany w osobnym Compose nadal wysyłamy w nagłówku `x-correlation-id`, ale w Tracking najlepiej użyć wartości dostępnej z triggera albo zapisać Correlation ID wcześniej w danych procesu.

Przykładowe expressions:

```text
ContractNumber = @{triggerBody()?['Title']}
ContractId     = @{triggerBody()?['ID']}
```

Jeżeli numer umowy jest zapisany w osobnej kolumnie `ContractNumber`, zamiast `Title` użyj jej wewnętrznej nazwy.

---

# Zadanie 5 – Sukces 201

Uruchom mock API w trybie `success` albo użyj numeru umowy bez `409` / `429` / `500` w nazwie.

Linux/macOS / Git Bash:

```bash
curl -s -X PUT "$API/admin/mode" \
  -H 'Content-Type: application/json' \
  -d '{"mode":"success"}'
```

PowerShell:

```powershell
$API = "https://<twoj-adres>.trycloudflare.com"

Invoke-RestMethod `
    -Method Put `
    -Uri "$API/admin/mode" `
    -ContentType "application/json" `
    -Body '{"mode":"success"}'
```

Sprawdzenie bieżącego trybu:

```powershell
Invoke-RestMethod "$API/admin/mode"
```

Reset pamięci mock API przed ponownym testem:

```powershell
Invoke-RestMethod `
    -Method Delete `
    -Uri "$API/api/contracts"
```

> Na wspólnym warsztacie bezpieczniej używać numerów `VCM/LAB04/201`, `409`, `429`, `500` niż globalnego `/admin/mode`. Zmiana globalnego trybu wpływa na wszystkich uczestników korzystających z tej samej instancji mock API.

Przykładowa odpowiedź:

```json
{
  "id": "ERP-10001",
  "status": "created"
}
```

Dodaj `Parse JSON` lub odczytaj odpowiedź przez expression.

Następnie `Update item`:

```text
ExternalSystemId = id
Status = Integrated
```

## Test

Sprawdź:

- Status HTTP,
- body odpowiedzi,
- zapis ExternalSystemId,
- nagłówek correlation ID.

---

# Zadanie 6 – Run after dla sukcesu

Dla `Update Contract - Integrated` ustaw Run after tak, aby wykonał się tylko, gdy HTTP zakończy się sukcesem.

W nowym designerze znajdź ustawienie Run after w konfiguracji akcji zależnej.

Sprawdź zaznaczenie:

```text
is successful
```

---

# Zadanie 7 – Obsługa 409 Conflict

Użyj numeru `VCM/LAB04/409`, nagłówka `x-mock-mode: 409` albo trybu globalnego `conflict`. Mock zwróci:

```text
409 Conflict
```

Przykładowy body:

```json
{
  "code": "CONTRACT_ALREADY_EXISTS",
  "message": "Contract already exists in external system",
  "externalId": "ERP-9999"
}
```

Dodaj Scope `Handle API Failure` i skonfiguruj **Run after** dla HTTP:

- has failed,
- has timed out.

W Scope:

1. odczytaj statusCode,
2. jeśli `409`:
   - potraktuj jako błąd biznesowy,
   - zapisz `ExternalSystemId`, jeżeli API go zwraca,
   - nie ponawiaj bezmyślnie requestu,
   - zapisz komunikat diagnostyczny.

Omów pojęcie idempotencji.

---

# Zadanie 8 – 429 Too Many Requests

Ustaw tryb `throttle`, nagłówek `x-mock-mode: 429` albo numer `VCM/LAB04/429`.

Przykładowo:

```text
HTTP 429
Retry-After: 10
```

## Test A – retry None

1. Ustaw Retry policy = None.
2. Uruchom flow.
3. Zanotuj:
   - liczbę prób,
   - czas wykonania,
   - rezultat.

## Test B – retry policy

1. Włącz retry policy.
2. Ustaw parametry zgodne z możliwościami akcji.
3. Ponownie uruchom test.
4. Porównaj Run History.

Pytania:

- Czy każdą operację można bezpiecznie ponowić?
- Co jeśli API stworzyło rekord, ale odpowiedź do Power Automate nie dotarła?
- Jak chronić się przed duplikatami?

---

# Zadanie 9 – 500 Internal Server Error

Ustaw tryb `error`, nagłówek `x-mock-mode: 500` albo numer `VCM/LAB04/500`.

Oczekiwane:

```text
HTTP failed
-> Handle API Failure
-> techniczny log
-> Contract nie otrzymuje statusu Integrated
```

Na tym etapie log może być zapisany w SharePoint lub Compose. Docelowy Process Log zbudujemy w LAB 09.

---

# Zadanie 10 – Expression do informacji o błędzie

W gałęzi błędu dodaj Compose:

```text
HTTP status
```

Przykład expression zależny od nazwy akcji:

```text
outputs('HTTP_-_Create_Contract')?['statusCode']
```

Body:

```text
body('HTTP_-_Create_Contract')
```

> Nazwa techniczna akcji może się różnić. Wybierz Peek code / expression helper lub dynamic content dostępne w designerze.

---

# Zadanie 11 – Test matrix

Wykonaj i udokumentuj:

| Test | HTTP | Retry | Oczekiwany rezultat |
|---|---:|---|---|
| A | 201 | dowolny | Integrated |
| B | 400 | None | techniczny/biznesowy błąd wg kontraktu API |
| C | 409 | None | obsłużony konflikt, brak ślepego retry |
| D | 429 | None | pojedynczy failure |
| E | 429 | retry | widoczne ponowienia |
| F | 500 | retry | failure po retry |

---

# Kryterium ukończenia

- uczestnik potrafi wskazać kartę Settings,
- potrafi skonfigurować Run after,
- rozumie retry i timeout,
- potrafi odróżnić 409 od 500,
- correlation ID jest wysyłane do API,
- przy 201 zapisywany jest ExternalSystemId.

## Po tym LAB

Talk track: retry classification, Failure Isolation. 409 i 500 nie mają tego samego retry.

---

# Najczęstsze błędy

## HTTP nie jest dostępne

Sprawdź licencję i DLP policy środowiska. Nie obchodź polityk organizacji przez inne konektory.

## Secure outputs ukryły dane

To zamierzone. Wyłącz ochronę wyłącznie w środowisku szkoleniowym, jeśli chcesz analizować odpowiedź.

## Retry powoduje duplikaty

To problem kontraktu integracyjnego. W produkcji stosuj idempotency key, business key lub endpoint typu upsert, jeżeli system zewnętrzny to obsługuje.

---

# Materiał Microsoft

- Cloud flows designer / Settings: https://learn.microsoft.com/en-us/power-automate/flows-designer
- Error handling guidance: https://learn.microsoft.com/en-us/power-automate/guidance/coding-guidelines/error-handling
- Secure data in cloud flows: https://learn.microsoft.com/en-us/power-automate/guidance/coding-guidelines/use-secure-inputs-outputs-triggers
