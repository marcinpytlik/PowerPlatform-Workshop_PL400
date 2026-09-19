# Power Automate – wzorce projektowe i zasady projektowania

## Dlaczego flow potrzebuje architektury

Power Automate bardzo łatwo zaczyna jako:

```text
Trigger -> kilka akcji -> gotowe
```

Po kilku miesiącach ten sam flow może mieć kilkadziesiąt akcji, wiele Condition, nested Apply to each i kilka miejsc z podobną logiką.

Wzorce pomagają uniknąć monolitycznych i trudnych do diagnozowania automatyzacji.

---

# 1. Orchestrator Pattern

## Idea

Jeden flow steruje procesem, ale nie implementuje całej logiki.

```text
Contract Submitted
        |
        v
   Orchestrator
   /    |      \
  v     v       v
Approval API Notification
```

## Orchestrator odpowiada za

- kolejność kroków,
- stan procesu,
- correlation ID,
- wywołanie child flows,
- agregację wyniku.

Nie powinien zawierać całej logiki domenowej każdego etapu.

---

# 2. Child Flow Pattern

## Idea

Wydziel powtarzalną lub niezależną funkcję do osobnego solution-aware child flow.

Przykłady:

```text
VCM - Approval
VCM - API Integration
VCM - Notification
VCM - Error Handler
```

## Korzyści

- ponowne użycie,
- prostsze testy,
- mniejsza liczba akcji w jednym flow,
- czytelniejszy Run History.

## Antywzorzec

Kopiowanie identycznego bloku Approval trzy razy.

---

# 3. Single Responsibility Flow

## Idea

Flow powinien mieć jedną główną odpowiedzialność.

Źle:

```text
Contract Created
+ approval
+ generowanie dokumentu
+ zapis PDF
+ integracja ERP
+ email
+ Teams
+ archiwizacja
```

Lepiej rozdzielić etapy i określić kontrakty pomiędzy nimi.

---

# 4. Trigger Guard Pattern

## Problem

Flow uruchamia się na każdą zmianę rekordu.

Następnie sam aktualizuje rekord i uruchamia się ponownie.

## Rozwiązanie

Użyj:

- Trigger Conditions,
- kolumny Status,
- flagi technicznej,
- filtrów triggera.

## VCM

Flow rozpoczyna właściwy proces tylko wtedy, gdy:

```text
Status = Submitted
```

---

# 5. Idempotency Pattern

## Idea

Ponowne wykonanie tego samego żądania nie powinno tworzyć kolejnych skutków ubocznych.

Przykład problemu:

```text
retry -> drugi POST -> dwa rekordy w ERP
```

## Rozwiązania

- correlation ID,
- idempotency key,
- alternate key,
- sprawdzenie istniejącego ExternalSystemId,
- deduplikacja.

## VCM

`Contract Number` + `Correlation ID` mogą być elementem kontraktu idempotencyjnego.

---

# 6. Retry with Classification

## Idea

Nie każdy błąd powinien być retry.

### Retry

- 429,
- transient 5xx,
- chwilowa niedostępność.

### Bez automatycznego retry

- 400,
- 401/403 bez oczekiwanej zmiany konfiguracji,
- 409 biznesowy,
- walidacja danych.

## Antywzorzec

Retry wszystkiego pięć razy.

---

# 7. TRY / CATCH / FINALLY

## Struktura

```text
TRY
 |
 +-- success
 |
 +-- failed/timed out
        |
        v
      CATCH
        |
        v
      FINALLY
        |
        v
Terminate if technical failure
```

## Zasada

Nie umieszczaj `Terminate Failed` w CATCH, jeżeli FINALLY ma się jeszcze wykonać.

---

# 8. Business Error vs Technical Error

## Business

```text
Approval rejected
409 duplicate contract
invalid business state
```

Run może zakończyć się technicznie sukcesem, mimo że proces biznesowy został odrzucony.

## Technical

```text
timeout
HTTP 500
connector failure
missing connection
```

To powinno być widoczne w monitoringu technicznym.

---

# 9. Correlation ID Pattern

Każdy proces dostaje identyfikator:

```text
guid()
```

Przenoś go przez:

- Contract,
- Approval,
- Process Log,
- request HTTP,
- child flows,
- komunikaty techniczne.

Dzięki temu jeden przypadek biznesowy można prześledzić przez wiele komponentów.

---

# 10. Append-only Process Log

## Idea

Nie nadpisuj jednego pola `LastError`.

Twórz kolejne rekordy:

```text
Timestamp
Flow Name
Run ID
Correlation ID
Action
Severity
HTTP Status
Error Code
Message
```

## Korzyść

Historia procesu nie ginie po kolejnym uruchomieniu.

---

# 11. Configuration over Hard-code

Nie umieszczaj bezpośrednio w flow:

- URL-i,
- adresów email,
- identyfikatorów środowiska,
- stałych biznesowych.

Używaj:

- Environment Variables,
- Dataverse configuration tables,
- Connection References.

---

# 12. Queue / Asynchronous Pattern

## Kiedy

Gdy użytkownik nie musi czekać na zakończenie procesu.

```text
App
 |
 v
Create Work Item
 |
 v
Async Flow
```

Przydatne dla:

- integracji,
- generowania dokumentów,
- ciężkich operacji,
- batch processing.

---

# 13. Fan-out / Fan-in

## Fan-out

Kilka niezależnych operacji może wykonać się równolegle:

```text
       +--> A
Start -+--> B
       +--> C
```

## Fan-in

Dalszy etap czeka na komplet wyników.

Uważaj na:

- limity connectorów,
- concurrency,
- kolejność zmian tego samego rekordu.

---

# 14. Saga-like Process Pattern

Power Automate nie jest pełnym silnikiem transakcyjnym.

Dla procesu wieloetapowego myśl o:

- krokach,
- stanie,
- kompensacji,
- retry,
- punktach nieodwracalnych.

Przykład:

```text
Approved
-> Integration Pending
-> ERP created
-> Notification failed
```

Nie próbuj „cofnąć” biznesowego approval tylko dlatego, że email się nie wysłał.

---

# 15. Compensating Action

Jeżeli nie możesz zrobić klasycznego rollbacku, wykonaj akcję kompensującą.

Przykład:

```text
utworzono rekord zewnętrzny
ale lokalny zapis końcowy nie powiódł się
```

Możliwe działania:

- oznaczenie do ręcznej rekonsyliacji,
- osobny retry,
- anulowanie operacji w systemie zewnętrznym, jeśli API to wspiera.

---

# 16. Circuit Breaker – koncepcja

Power Automate nie implementuje automatycznie klasycznego circuit breakera jak biblioteki resilience.

Możesz jednak zaprojektować flagę konfiguracyjną:

```text
VCM_ENABLE_EXTERNAL_INTEGRATION = false
```

Gdy zewnętrzny system jest niestabilny, nowe procesy trafiają do stanu oczekującego zamiast generować tysiące nieudanych requestów.

---

# 17. Dead-letter / Manual Intervention Pattern

Nie każdy przypadek da się naprawić automatycznie.

Twórz stan:

```text
Integration Error
Needs Manual Review
```

oraz kolejkę przypadków do ręcznej obsługi.

To jest lepsze niż nieskończony retry.

---

# 18. Anti-patterns w Power Automate

Unikaj:

- monolitycznego flow z setkami akcji,
- nested Condition 5–6 poziomów,
- kopiowania tych samych bloków,
- aktualizacji rekordu wyzwalającej ten sam flow bez guard condition,
- retry błędów biznesowych,
- hard-code URL-i i maili,
- braku correlation ID,
- braku logowania,
- Apply to each uruchamianego na tysiącach elementów bez kontroli,
- równoległych aktualizacji tego samego rekordu bez strategii concurrency,
- traktowania Run History jako jedynego audytu biznesowego.

---

# Checklista projektowa Power Automate

1. Czy flow ma jedną odpowiedzialność?
2. Czy trigger może uruchomić się ponownie przez własny Update?
3. Czy proces jest idempotentny?
4. Czy retry dotyczy tylko błędów transient?
5. Czy mamy correlation ID?
6. Czy błędy biznesowe są odróżnione od technicznych?
7. Czy konfiguracja jest poza flow?
8. Czy log techniczny jest append-only?
9. Czy child flow poprawiłby czytelność?
10. Czy znamy zachowanie przy concurrency?
11. Czy istnieje manual recovery path?
12. Czy użytkownik musi czekać, czy proces może być async?

---

# Materiały Microsoft

- Power Automate reference architectures: https://learn.microsoft.com/en-us/power-platform/architecture/products/power-automate
- Power Platform Architecture Center: https://learn.microsoft.com/en-us/power-platform/architecture/
