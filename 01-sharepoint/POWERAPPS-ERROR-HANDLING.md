# Power Apps – obsługa błędów

## Cel dokumentu

Dokument opisuje podstawowe wzorce obsługi błędów w Canvas Apps.

## 1. Notify to za mało

`Notify()` informuje użytkownika, ale nie jest pełnym mechanizmem error handling.

Aplikacja powinna rozróżniać:

- sukces,
- błąd walidacji,
- błąd źródła danych,
- brak uprawnień,
- timeout,
- konflikt stanu.

## 2. IfError

`IfError()` pozwala kontrolować błąd wykonania formuły.

Przykład:

```powerfx
IfError(
    Patch(...),
    Notify("Nie udało się zapisać danych", NotificationType.Error)
)
```

## 3. Errors()

`Errors()` pozwala odczytać błędy źródła danych.

Może być użyteczne przy bardziej szczegółowej diagnostyce zapisu.

## 4. Patch i sukces

Nie należy zakładać, że samo wywołanie `Patch()` oznacza poprawny zapis.

Po operacji warto jawnie obsłużyć sukces i błąd.

## 5. Optimistic UI

Optimistic UI zakłada sukces zanim backend go potwierdzi.

Może poprawić UX, ale zwiększa ryzyko rozjazdu stanu.

## 6. Confirmed State

Przy procesach krytycznych lepiej potwierdzić wynik zapisu po stronie backendu przed pokazaniem użytkownikowi finalnego stanu.

## 7. Walidacja

Walidację należy rozdzielać na:

- klienta,
- backend,
- reguły procesu.

UI nie powinno być jedynym miejscem zapewniającym poprawność danych.

## 8. Refresh po zapisie

Nie zawsze trzeba odświeżać całe źródło.

Lepsze może być użycie zwróconego rekordu z `Patch()` lub aktualizacja lokalnego stanu.

## 9. Błędy techniczne i biznesowe

Przykład:

```text
Kwota < 0
   -> błąd walidacji biznesowej

SharePoint 403
   -> błąd uprawnień

SharePoint 429
   -> throttling

timeout
   -> błąd techniczny
```

## 10. Logowanie

Dla krytycznych aplikacji warto używać:

- Trace,
- correlation ID,
- backendowego Process Log,
- Live Monitor.

## 11. Anti-patterny

- samo `Notify("Error")`,
- brak rozróżnienia typów błędów,
- natychmiastowa nawigacja po Patch bez sprawdzenia wyniku,
- ukrywanie błędów technicznych,
- brak korelacji z backendem.
