# Power Apps + SharePoint Online – delegacja

## Cel dokumentu

Dokument opisuje delegację zapytań Power Apps do SharePoint Online, typowe pułapki oraz zasady projektowania formuł, które pozostają poprawne przy rosnącym wolumenie danych.

## 1. Czym jest delegacja

Delegacja oznacza wykonanie operacji przez źródło danych.

```text
Power Apps
   |
   v
SharePoint wykonuje filtr / sortowanie
   |
   v
Power Apps pobiera wynik
```

Przy wyrażeniu niedelegowalnym część danych jest pobierana lokalnie i przetwarzana po stronie klienta.

## 2. Limit 500 / 2000

Domyślny limit lokalnego przetwarzania danych niedelegowalnych wynosi 500 rekordów.

Można go zwiększyć maksymalnie do 2000.

Zwiększenie limitu nie naprawia niedelegowalnego zapytania.

## 3. Delegacja jako problem poprawności

Przykład:

```text
Lista: 100 000 rekordów
Szukany rekord: pozycja 35 000
Zapytanie: niedelegowalne
Limit lokalny: 500
```

Aplikacja może zwrócić 0 wyników mimo że rekord istnieje.

Delegation warning może więc oznaczać niepełny wynik, a nie tylko gorszą wydajność.

## 4. Filter

`Filter()` nie jest automatycznie delegowalny.

Delegowalność zależy od:

- źródła danych,
- operatora,
- typu kolumny,
- całego wyrażenia.

## 5. LookUp

`LookUp()` również należy oceniać w kontekście konkretnego źródła i warunku.

Typowy problem to wywołanie `LookUp()` osobno dla każdego wiersza galerii.

```text
Gallery 100 rekordów
+
100 dodatkowych LookUp()
```

To może prowadzić do problemu N+1.

## 6. StartsWith

`StartsWith()` bywa dobrym narzędziem do delegowalnego wyszukiwania tekstowego, ale należy weryfikować delegację dla konkretnego typu kolumny.

## 7. IsBlank

`IsBlank()` może zachowywać się inaczej zależnie od źródła i typu pola.

W praktyce należy zawsze sprawdzić ostrzeżenie delegacji dla konkretnej formuły.

## 8. SharePoint ID

Pole `ID` jest polem systemowym.

Prosty warunek:

```powerfx
Filter(Contracts, ID = 123)
```

jest innym przypadkiem niż zakresy i złożone porównania po ID.

## 9. Choice

Choice jest typem złożonym.

Typowy dostęp:

```powerfx
Status.Value
```

Nie należy traktować Choice identycznie jak zwykłego tekstu.

## 10. Person / Group

Person / Group może zawierać m.in.:

```text
DisplayName
Email
Claims
Department
JobTitle
```

Nie wszystkie operacje na wszystkich właściwościach delegują się tak samo.

## 11. Lookup

Lookup zawiera najczęściej:

```text
Id
Value
```

Porównanie po `Id` i po `Value` to różne operacje.

## 12. Delegacja a galerie

Galeria nie powinna pobierać więcej danych niż potrzebuje użytkownik.

Dobre podejście:

```text
Filter at source
+
delegowalne sortowanie
+
ograniczony zestaw pól
```

## 13. Anti-patterny

- `ClearCollect(BigList)` jako sposób na usunięcie warningu.
- Ładowanie całej listy w `App.OnStart`.
- `LookUp()` w każdym rekordzie galerii.
- Ignorowanie delegation warningów.
- Testowanie aplikacji tylko na 20 rekordach.

## 14. Dobre praktyki

- Testować na realistycznym wolumenie danych.
- Projektować formuły z myślą o delegacji od początku.
- Filtrować jak najbliżej źródła.
- Korzystać z indeksów SharePoint.
- Sprawdzać delegację po zmianie typu kolumny lub formuły.
- Traktować warning jako problem poprawności, nie tylko wydajności.

## 15. Dokumentacja

- https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/delegation-overview
- https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/connections/connection-sharepoint-online
