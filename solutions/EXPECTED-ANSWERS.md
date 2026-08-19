# Oczekiwane kierunki rozwiązań

## E02 – Idempotency
- alternate/external key,
- kontrola ExternalSystemId,
- correlation/request ID,
- API przyjmujące idempotency key, jeżeli wspierane.

## E03 – Trigger loop
- trigger conditions,
- pole techniczne/status procesu,
- rozdzielenie zdarzeń biznesowych od technicznych aktualizacji,
- dodatkowa kontrola poprzedniego i nowego stanu.

## E05 – Error classification
- Business: nie retry automatycznie, czytelny status biznesowy.
- Transient: retry/backoff.
- Technical: log, alert i kontrolowane zakończenie.

## E06 – Architecture
Rozważyć Azure Function lub inną warstwę kodową, szczególnie jeśli flow staje się silnikiem transformacji zamiast orkiestratorem procesu.
