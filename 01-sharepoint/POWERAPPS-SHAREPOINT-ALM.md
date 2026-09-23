# Power Apps + SharePoint Online – ALM i środowiska

## Cel

Dokument opisuje podstawowy lifecycle aplikacji Canvas korzystającej z SharePoint Online.

## 1. Problem prostego developmentu

Model:

```text
developer tworzy app
-> connection na jego koncie
-> URL listy wpisany ręcznie
-> publish
```

jest szybki, ale słabo skaluje się do TEST/PROD i utrzymania zespołowego.

## 2. DEV / TEST / PROD

Środowiska powinny mieć jawne role:

```text
DEV  -> development
TEST -> walidacja
PROD -> użytkownicy końcowi
```

Nie testuj nowych zmian bezpośrednio na produkcyjnej aplikacji.

## 3. SharePoint jako zależność środowiskowa

SharePoint nie zachowuje się tak samo jak tabele Dataverse wewnątrz Solution.

Trzeba świadomie zarządzać:

- Site URL,
- nazwami list,
- schematem kolumn,
- internal names,
- uprawnieniami.

## 4. Konfiguracja

Nie hard-code konfiguracji środowiskowej w wielu formułach.

Przykładowe wartości:

```text
Site URL
API Base URL
Support Email
Feature Flags
```

powinny mieć jedno kontrolowane źródło.

## 5. Solutions

Canvas App i flow powinny być przenoszone przez Solutions tam, gdzie jest to możliwe.

Korzyści:

- wersjonowanie,
- zależności,
- import/export,
- Connection References,
- Environment Variables.

## 6. Connection References

Flow wewnątrz Solution powinien używać Connection References.

Nie utożsamiaj Connection Reference z samym connection użytkownika.

Reference jest artefaktem rozwiązania wskazującym na connection skonfigurowane w danym środowisku.

## 7. Environment Variables

Environment Variables nadają się m.in. do:

- API URL,
- identyfikatorów lub URL zasobów,
- wartości konfiguracyjnych.

Nie przechowuj w nich sekretów w zwykłym tekście.

## 8. Tożsamości techniczne

Proces produkcyjny nie powinien zależeć od prywatnego connection developera.

Dla flow backendowego rozważ dedykowaną tożsamość techniczną zgodnie z polityką organizacji.

## 9. Provisioning SharePoint

Jeżeli rozwiązanie wymaga konkretnych list, kolumn i indeksów, ich provisioning powinien być udokumentowany lub zautomatyzowany.

Minimum dokumentacji:

```text
List
Column
Internal Name
Type
Required
Default
Indexed
Lookup target
```

## 10. Deployment checklist

```text
[ ] rozwiązanie zaimportowane
[ ] Connection References skonfigurowane
[ ] Environment Variables ustawione
[ ] listy SharePoint istnieją
[ ] schemat list zgodny
[ ] grupy security skonfigurowane
[ ] app shared
[ ] flow enabled
[ ] smoke test
```

## 11. Rollback

Rollback powinien obejmować więcej niż samą wersję Canvas App.

Zmiany schematu SharePoint, flow i API mogą być niekompatybilne z wcześniejszą aplikacją.

## 12. Ownership

Dokumentuj:

- owner aplikacji,
- co-owner,
- owner flow,
- technical connection,
- owner list SharePoint,
- kontakt supportowy.

## 13. Zasada

ALM zaczyna się przed pierwszym deploymentem, nie po pojawieniu się środowiska produkcyjnego.
