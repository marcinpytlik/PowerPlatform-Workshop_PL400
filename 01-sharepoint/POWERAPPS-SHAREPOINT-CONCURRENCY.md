# Power Apps + SharePoint Online – współbieżność i konflikty zapisu

## Cel

Dokument opisuje problem dwóch lub większej liczby użytkowników modyfikujących ten sam rekord.

## 1. Problem

Scenariusz:

```text
10:00 Marcin otwiera Contract 123
10:01 Heniek otwiera Contract 123
10:05 Marcin zapisuje Amount = 100000
10:06 Heniek zapisuje Status = Submitted
```

Jeżeli zapis Heńka wysyła również starą wartość Amount, może dojść do utraty zmiany Marcina.

## 2. Lost update

Lost update występuje, gdy późniejszy zapis nadpisuje zmianę wykonaną wcześniej przez innego użytkownika.

SharePoint nie jest klasycznym systemem transakcyjnym dla procesu wieloetapowego.

## 3. Partial update

Jeżeli zmieniasz tylko Status, nie wysyłaj całego rekordu bez potrzeby.

Power Apps `Patch()` i SharePoint REST partial update pomagają ograniczać powierzchnię konfliktu.

## 4. Refresh przed krytyczną operacją

Przed zmianą wymagającą aktualnego stanu można:

```powerfx
Refresh(Contracts)
```

i ponownie odczytać rekord.

Nie eliminuje to wszystkich race conditions, ale zmniejsza ryzyko pracy na starych danych.

## 5. Status jako state machine

Operacja powinna sprawdzać bieżący status:

```text
Draft -> Submitted
Submitted -> In Approval
In Approval -> Approved
```

Nie wykonuj:

```text
dowolny status -> Approved
```

bez walidacji stanu.

## 6. ETag w SharePoint REST

SharePoint REST obsługuje kontrolę wersji przez ETag.

```text
IF-MATCH: *
```

akceptuje dowolną bieżącą wersję.

Dla optimistic concurrency można użyć konkretnego ETag i odrzucić zapis, jeśli rekord zmienił się od odczytu.

## 7. Konflikt jako normalny scenariusz

Konflikt nie powinien kończyć się przypadkowym nadpisaniem.

Aplikacja może:

- poinformować użytkownika,
- odświeżyć rekord,
- pokazać aktualne dane,
- poprosić o ponowne zastosowanie zmiany.

## 8. Flow i concurrency

Dwa flowy aktualizujące ten sam element mogą powodować race condition.

Szczególnie niebezpieczne jest wiele flowów będących właścicielami tej samej kolumny Status.

## 9. Concurrency Control w Power Automate

Ograniczenie równoległości może być pomocne, ale nie zastępuje poprawnego modelu procesu.

Globalne ustawienie concurrency = 1 może zmniejszyć przepustowość.

## 10. Wzorzec właściciela stanu

Preferowany model:

```text
jeden orchestrator
-> waliduje przejście
-> aktualizuje Status
```

inne flowy zapisują własne dane techniczne, ale nie walczą o ten sam stan biznesowy.

## 11. Kiedy SharePoint przestaje wystarczać

Jeżeli aplikacja wymaga:

- silnej optimistic concurrency,
- transakcyjności,
- wielu równoległych edycji,
- rozbudowanych reguł integralności,

należy rozważyć Dataverse, SQL lub API jako backend.
