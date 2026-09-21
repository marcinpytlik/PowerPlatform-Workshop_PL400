# SharePoint Online, Power Apps i Power Automate – bezpieczeństwo i połączenia

## Cel dokumentu

Dokument opisuje różnice pomiędzy uprawnieniami użytkownika, sharingiem aplikacji oraz kontami używanymi przez connection w Power Automate.

## 1. Power Apps i kontekst użytkownika

Canvas App korzystająca bezpośrednio z SharePoint zwykle działa w kontekście użytkownika.

Użytkownik musi mieć odpowiednie uprawnienia do źródła danych.

Samo udostępnienie aplikacji nie oznacza automatycznie udostępnienia wszystkich źródeł danych.

## 2. Sharing aplikacji vs sharing SharePoint

To dwa różne mechanizmy.

```text
App shared
!=
SharePoint permissions granted
```

Użytkownik może mieć dostęp do aplikacji, ale nie do listy, z której aplikacja korzysta.

## 3. Power Automate i connection owner

Flow może wykonywać akcje przez connection należące do określonego konta.

To oznacza, że flow może mieć większe uprawnienia niż użytkownik inicjujący proces.

Taki model może być poprawny, ale musi być świadomie zaprojektowany.

## 4. Service account / technical identity

Współdzielone procesy nie powinny bez potrzeby zależeć od prywatnego konta developera.

Ryzyka:

- odejście użytkownika,
- wygasłe hasło,
- odebrane licencje,
- zmiana MFA,
- brak właściciela procesu.

## 5. Least privilege

Connection techniczne powinno mieć minimalny zestaw wymaganych uprawnień.

Nie należy przyznawać Full Control tylko dlatego, że upraszcza development.

## 6. Item-level permissions

Indywidualne uprawnienia elementów są możliwe, ale zwiększają liczbę security scopes.

Przy dużej liczbie rekordów model może stać się kosztowny.

## 7. Broken inheritance

Łamanie dziedziczenia dla tysięcy rekordów wymaga ostrożności.

Lepszym modelem może być:

- podział danych,
- folder-level permissions,
- osobne listy,
- Dataverse security,
- inny model domenowy.

## 8. "Run-only users"

Przy flowach wywoływanych ręcznie trzeba rozumieć, czy akcje korzystają z connection właściciela czy użytkownika uruchamiającego.

Model powinien być spójny z wymaganiami bezpieczeństwa.

## 9. Connection References

W Solution connection powinny być reprezentowane przez Connection References.

Pozwala to odłączyć lifecycle rozwiązania od prywatnego connection developera.

## 10. DLP

Data Loss Prevention Policies mogą ograniczać:

- HTTP,
- custom connectors,
- łączenie connectorów Business i Non-Business,
- użycie wybranych usług.

Błąd aplikacji lub flow może więc wynikać z polityki środowiska, a nie z samego kodu.

## 11. Sekrety

Sekretów nie należy przechowywać:

- w Power Fx,
- w zwykłych zmiennych tekstowych,
- w bundle SPFx,
- w komentarzach,
- w opisach flow.

## 12. Audyt

SharePoint version history i auditing Power Platform rozwiązują inne problemy.

Warto rozdzielić:

- kto zmienił rekord,
- jaki flow wykonał operację,
- jakie connection zostało użyte,
- jaki był correlation ID.

## 13. Checklista

- Czy użytkownik ma dostęp do źródła danych?
- Czy sharing aplikacji jest zgodny z uprawnieniami SharePoint?
- Na czyim connection działa flow?
- Czy proces zależy od prywatnego konta?
- Czy connection ma minimalne uprawnienia?
- Czy item-level permissions nie rosną nadmiernie?
- Czy DLP pozwala na wymagane connectory?
