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

90 minut.

## Wymagania

- ukończony LAB 03,
- endpoint demonstracyjny prowadzącego lub mock API,
- możliwość użycia akcji HTTP w środowisku szkoleniowym.

> Akcja HTTP może wymagać odpowiedniej licencji. Jeżeli tenant jej nie udostępnia, prowadzący może wykonać demo, a uczestnicy przeanalizować flow i payload.

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

# Zadanie 1 – Przygotowanie requestu

Dodaj Scope `External Integration` po końcowym Approved.

Dodaj Compose `Compose - API Request`:

```json
{
  "contractNumber": "@{triggerBody()?['Title']}",
  "supplier": "<supplier name>",
  "amount": "<amount>",
  "currency": "<currency>",
  "correlationId": "<correlation id>"
}
```

W designerze nie wklejaj literalnie placeholderów `<...>` – wybierz dynamic content z flow.

## Cel

Request ma być widoczny jako osobny krok przed HTTP. Ułatwia to diagnostykę i pozwala odróżnić błąd budowy payloadu od błędu wywołania API.

---

# Zadanie 2 – Akcja HTTP

Dodaj akcję `HTTP`.

Ustaw:

```text
Method: POST
URI: <endpoint prowadzącego>/api/contracts
```

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

# Zadanie 3 – Settings akcji

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

Dodaj do tracked properties:

```text
ContractNumber
CorrelationId
```

Wartości wybierz z dynamic content/expressions.

---

# Zadanie 4 – Sukces 201

Uruchom endpoint w trybie zwracającym 201.

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

# Zadanie 5 – Run after dla sukcesu

Dla `Update Contract - Integrated` ustaw Run after tak, aby wykonał się tylko, gdy HTTP zakończy się sukcesem.

W nowym designerze znajdź ustawienie Run after w konfiguracji akcji zależnej.

Sprawdź zaznaczenie:

```text
is successful
```

---

# Zadanie 6 – Obsługa 409 Conflict

Skonfiguruj mock API tak, aby dla konkretnego ContractNumber zwracało:

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

# Zadanie 7 – 429 Too Many Requests

Ustaw endpoint w trybie 429.

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

# Zadanie 8 – 500 Internal Server Error

Ustaw API w trybie 500.

Oczekiwane:

```text
HTTP failed
-> Handle API Failure
-> techniczny log
-> Contract nie otrzymuje statusu Integrated
```

Na tym etapie log może być zapisany w SharePoint lub Compose. Docelowy `ProcessLog` zbudujemy w LAB 08.

---

# Zadanie 9 – Expression do informacji o błędzie

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

# Zadanie 10 – Test matrix

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
