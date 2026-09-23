# Power Apps + SharePoint Online – testowanie i wydanie

## Cel

Dokument opisuje minimalny proces techniczny przed publikacją Canvas App.

## 1. Test na koncie developera jest niewystarczający

Developer często ma:

- Owner/Full Control SharePoint,
- Environment Maker,
- szerokie connection,
- dostęp do wszystkich list.

Aplikację trzeba testować także kontem zwykłego użytkownika.

## 2. Minimalne scenariusze

Sprawdź:

- start aplikacji,
- odczyt list,
- wyszukiwanie,
- filtrowanie,
- create,
- update,
- delete jeśli występuje,
- błędy walidacji,
- brak dostępu,
- działanie flow,
- zachowanie przy błędzie backendu.

## 3. App Checker

Uruchamiaj App Checker przed publikacją.

Nie wszystkie ostrzeżenia są blockerem, ale każde powinno być świadomie ocenione.

## 4. Live Monitor

Live Monitor pomaga znaleźć:

- wolne requesty,
- błędy connectora,
- nadmiarowe wywołania,
- problemy z delegacją,
- N+1.

## 5. Test delegacji

Test na 20 rekordach nie wykryje problemów delegacji.

Przygotuj dane większe niż non-delegable row limit i sprawdź wynik.

## 6. Test security

Utwórz użytkownika testowego z minimalnymi prawami.

Sprawdź aplikację po:

- odebraniu Edit,
- pozostawieniu Read,
- odebraniu dostępu do jednej listy,
- zmianie membership grupy.

## 7. Publish

Save i Publish to różne operacje.

Zmiany robocze nie stają się wersją używaną przez wszystkich dopóki nie zostaną opublikowane.

## 8. Versioning i restore

Przed większą zmianą zanotuj wersję aplikacji.

Restore jest mechanizmem awaryjnym, nie strategią ALM.

## 9. Smoke test po publikacji

Po publikacji wykonaj:

```text
launch
-> read
-> create/update
-> flow
-> expected status
```

na koncie użytkownika.

## 10. Regression checklist

Zmiana jednego ekranu może wpłynąć na:

- formularz,
- gallery,
- zmienne,
- flow,
- security,
- performance.

Utrzymuj checklistę regresji dla krytycznych ścieżek.

## 11. Dane testowe

Nie używaj produkcyjnych danych osobowych do testów developerskich.

Przygotuj przewidywalny zestaw rekordów reprezentujący:

- happy path,
- edge cases,
- duże wartości,
- brakujące wartości,
- konflikty.

## 12. Definition of Done

Przykład:

```text
[ ] App Checker przejrzany
[ ] brak krytycznych błędów Monitor
[ ] test zwykłego użytkownika
[ ] test delegacji
[ ] test flow
[ ] test błędu backendu
[ ] publikacja
[ ] smoke test
[ ] dokumentacja zmiany
```
