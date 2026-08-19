# Projekt flowów

## VCM - Contract Created

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
- zapis ProcessLog,
- powiadomienie techniczne.
