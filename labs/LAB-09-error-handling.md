# LAB 09 – Error handling: TRY / CATCH / FINALLY i ProcessLog

## Cel laboratorium

Przebudować flow integracyjne do wzorca, który można utrzymywać w środowisku produkcyjnym.

Po laboratorium uczestnik potrafi:

- grupować akcje w Scopes,
- konfigurować Run after,
- normalizować kontekst błędu,
- zapisywać błędy do Dataverse Process Log,
- rozróżnić błąd biznesowy i techniczny,
- świadomie używać `Terminate`,
- zbudować FINALLY.

## Czas

90 minut. W agendzie 3-dniowej: **75 min** – testy 201, 500 i Terminate po FINALLY. Timeout zostaw, jeśli jest bufor.

## Wymagania

- LAB 04 oraz LAB 06,
- tabela Process Log i Contract w Dataverse,
- mock API w trybie `success`, potem `error`.

---

# Wzorzec

```text
Trigger
 |
 v
Scope TRY
 |   +-- validation
 |   +-- approval/integration
 |   +-- update business data
 |
 +------ success ------>
 |
 v
Scope CATCH
 |   +-- collect context
 |   +-- create ProcessLog
 |   +-- update technical status
 |   +-- notify support
 |
 v
Scope FINALLY
     +-- final telemetry / cleanup
```

---

# Zadanie 1 – Kopia flow

Nie przebudowuj jedynego działającego flow bez punktu odniesienia.

1. Otwórz flow z LAB 04.
2. Zapisz kopię lub utwórz nową wersję w Solution.
3. Nazwa:

```text
VCM - Contract Integration - v2
```

---

# Zadanie 2 – Scope TRY

Dodaj `Scope` i nazwij:

```text
TRY - Process Contract
```

Przenieś do środka:

- Compose request,
- HTTP,
- Parse JSON,
- Update Contract,
- inne akcje należące do głównej logiki.

Nie umieszczaj w TRY obsługi błędów.

---

# Zadanie 3 – Scope CATCH

Dodaj Scope po TRY:

```text
CATCH - Technical Error
```

Otwórz **Run after** dla CATCH.

Zaznacz:

```text
has failed
has timed out
```

Opcjonalnie `is skipped`, jeżeli architektura danego flow wymaga przechwycenia przerwanej ścieżki.

Nie zaznaczaj `is successful`.

---

# Zadanie 4 – Scope FINALLY

Dodaj Scope:

```text
FINALLY - Complete
```

Skonfiguruj Run after tak, aby wykonał się po:

- sukcesie TRY,
- sukcesie lub zakończeniu CATCH.

W praktyce możesz skonfigurować FINALLY jako zależny od obu Scopes lub zastosować układ liniowy, w którym CATCH jest skipped przy sukcesie, a FINALLY uruchamia się dla odpowiednich statusów poprzedniego elementu.

Cel: FINALLY ma wykonać się niezależnie od ścieżki biznesowej, o ile flow nie zostało wcześniej bezwarunkowo zakończone przez Terminate.

---

# Zadanie 5 – Kontekst błędu

W CATCH dodaj Compose `Compose - Error Context`.

Docelowy logiczny rekord:

```json
{
  "flowName": "VCM - Contract Integration - v2",
  "flowRunId": "...",
  "correlationId": "...",
  "contractNumber": "...",
  "contractId": "...",
  "timestamp": "...",
  "actionName": "HTTP - Create Contract",
  "httpStatus": 500,
  "errorCode": "...",
  "message": "..."
}
```

## Flow Run ID

Użyj workflow expression odpowiedniej dla środowiska, np. danych z `workflow()`.

Podczas szkolenia wyświetl wynik `workflow()` w Compose i znajdź `run.name`.

## Timestamp

```text
utcNow()
```

## Correlation ID

Użyj ID utworzonego wcześniej i przechowywanego w Contract.

---

# Zadanie 6 – Result funkcji Scope

W CATCH dodaj Compose:

```text
Result TRY
```

Expression:

```text
result('TRY_-_Process_Contract')
```

> Techniczna nazwa Scope może różnić się od wyświetlanej. Wstaw expression zgodnie z nazwą w designerze.

Uruchom flow z błędem 500 i zobacz strukturę wyniku.

Znajdź:

- name,
- status,
- error/code,
- error/message.

To pozwala budować bardziej ogólny error handler zamiast hard-code dla jednej akcji HTTP.

---

# Zadanie 7 – Utworzenie Process Log

W CATCH dodaj Dataverse `Add a new row` dla table Process Log.

Mapowanie:

```text
Flow Name       <- nazwa flow
Flow Run ID     <- workflow().run.name
Correlation ID  <- correlation ID
Timestamp       <- utcNow()
Action Name     <- nazwa failed action lub wartość ustalona dla LAB
Severity        <- Error
HTTP Status     <- status HTTP, jeśli istnieje
Error Code      <- normalized error code
Message         <- error message
Contract        <- lookup do bieżącej umowy
```

Lookup Contract jest wymagany. Po LAB 06 proces pracuje na Dataverse – nie zapisuj logu „w powietrze”.

---

# Zadanie 8 – Aktualizacja stanu biznesowego

W CATCH ustaw Contract:

```text
Status = Integration Error
```

Nie nadpisuj poprawnych danych takich jak Supplier, Amount czy daty.

Pytanie:

> Czy błąd techniczny powinien cofać umowę z Approved do Draft?

Oczekiwana odpowiedź: zazwyczaj nie. Stan biznesowy i stan technicznej integracji warto rozdzielić lub przynajmniej modelować świadomie.

---

# Zadanie 9 – Powiadomienie techniczne

Dodaj email lub Teams zgodnie z polityką środowiska.

Subject:

```text
[VCM][ERROR] <ContractNumber> - <CorrelationId>
```

Treść:

- Flow name,
- Flow run ID,
- Contract number,
- Correlation ID,
- Timestamp,
- HTTP status,
- Error message.

Nie wysyłaj w email pełnych sekretów/request body, jeśli zawierają dane wrażliwe.

---

# Zadanie 10 – Flaga błędu technicznego

W CATCH ustaw zmienną logiczną, np.:

```text
varTechnicalError = true
```

Nie używaj jeszcze `Terminate`. Akcja Terminate kończy run, więc umieszczona w CATCH uniemożliwiłaby wykonanie FINALLY.

Omów różnicę:

- Rejected approval = prawidłowe zakończenie procesu biznesowego,
- HTTP 500 = failure techniczny.

Nie oznaczaj odrzuconej umowy jako failed flow tylko dlatego, że użytkownik wybrał Reject.

---

# Zadanie 11 – FINALLY

W FINALLY dodaj wpis informacyjny lub Compose:

```text
Process finished at <utcNow()>
```

W bardziej rozbudowanym wariancie FINALLY może:

- wyczyścić tymczasowe dane,
- zapisać telemetry event,
- zwolnić lock logiczny,
- wyzerować flagę `Processing`.

---

# Zadanie 12 – Zakończenie technicznego failure

**Po FINALLY** dodaj Condition:

```text
varTechnicalError = true
```

Dla Yes dodaj `Terminate`:

```text
Status = Failed
Code = VCM_TECHNICAL_ERROR
```

Dzięki temu FINALLY wykonuje się zarówno po sukcesie, jak i po błędzie, a końcowy status runu nadal poprawnie sygnalizuje awarię techniczną.

---

# Testy

## Test 1 – 201

Oczekiwane:

```text
TRY succeeded
CATCH skipped
FINALLY succeeded
Contract = Integrated
```

## Test 2 – 500

Oczekiwane:

```text
TRY failed
CATCH succeeded
ProcessLog created
Contract = Integration Error
FINALLY succeeded
flow final status = Failed
```

## Test 3 – timeout

Ustaw endpoint opóźniający odpowiedź ponad timeout.

Oczekiwane: CATCH wykona się dla Timed out.

---

# Kryterium ukończenia

- TRY/CATCH/FINALLY są czytelnie nazwane,
- CATCH działa dla Failed i Timed out,
- powstaje rekord ProcessLog,
- zawiera FlowRunId i CorrelationId,
- stan Contract odzwierciedla błąd integracji,
- techniczny failure kończy flow jako Failed.

---

# Materiał Microsoft

- Robust error handling: https://learn.microsoft.com/en-us/power-automate/guidance/coding-guidelines/error-handling
- Cloud flow designer: https://learn.microsoft.com/en-us/power-automate/flows-designer
