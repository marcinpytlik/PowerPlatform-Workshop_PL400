# Projekt flowów

## VCM - Contract Submitted

Orchestrator. W LAB 03–04 jako `VCM - Contract Submitted - SP`, od LAB 06 na Dataverse. LAB 09 zapisuje kopię `VCM - Contract Submitted - v2`.

Odpowiedzialność:

- walidacja danych wejściowych,
- utworzenie correlation ID,
- uruchomienie procesu akceptacji.

## VCM - Approval

Odpowiedzialność:

- wybór wymaganych poziomów akceptacji,
- rejestr decyzji,
- przekazanie sterowania dalej.

## VCM - API Integration

Odpowiedzialność:

- budowa requestu,
- HTTP,
- obsługa odpowiedzi,
- retry/throttling,
- zapis identyfikatora z systemu zewnętrznego.

## VCM - Notification

Odpowiedzialność:

- powiadomienia użytkowników.

## VCM - Error Handler

Odpowiedzialność:

- normalizacja informacji o błędzie,
- zapis Process Log,
- powiadomienie techniczne.


---

## Dalej: wzorce projektowe

Przejdź do [DESIGN-PATTERNS.md](DESIGN-PATTERNS.md), gdzie opisane są m.in. Orchestrator, Child Flow, Trigger Guard, Idempotency, retry classification, Saga-like process, compensating actions i observability.
