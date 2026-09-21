# SharePoint Online jako backend dla Power Apps i Power Automate

## Cel dokumentu

Dokument opisuje najważniejsze ograniczenia SharePoint Online w kontekście używania list i bibliotek jako źródła danych dla Power Apps oraz Power Automate.

SharePoint Online może przechowywać bardzo duże ilości danych, ale jego limity pojemnościowe nie są tym samym co limity operacyjne. W praktyce o jakości rozwiązania decydują jednocześnie:

- liczba elementów,
- sposób filtrowania,
- indeksy,
- delegacja Power Apps,
- liczba lookupów,
- model uprawnień,
- sposób użycia Power Automate,
- throttling,
- liczba równoległych procesów,
- sposób modelowania relacji i stanu procesu.

---

# 1. Najważniejsze limity

| Obszar | Limit / rekomendacja | Znaczenie |
|---|---:|---|
| Elementy w liście | 30 000 000 | maksymalna skala listy |
| Pliki i foldery w bibliotece | 30 000 000 | maksymalna skala biblioteki |
| List View Threshold | 5 000 | próg operacyjny widoków i zapytań |
| Unique security scopes | 50 000 | techniczny limit dla listy / biblioteki |
| Zalecane unique security scopes | poniżej 5 000 | lepsza wydajność i prostsze utrzymanie |
| Elementy a zmiana inheritance | 100 000 | po przekroczeniu pojawiają się ograniczenia zmiany dziedziczenia |
| Rozmiar pliku w bibliotece | 250 GB | pojedynczy plik |
| Załącznik do elementu listy | 250 MB | attachment list item |
| Długość ścieżki | 400 znaków | pełna ścieżka pliku |
| Major versions | 50 000 | liczba wersji głównych |
| Minor versions | 511 | liczba wersji roboczych |
| Zalecana skala synchronizacji | ok. 300 000 plików | rekomendacja wydajnościowa OneDrive Sync |
| Cross-site move/copy | 30 000 plików / 100 GB | pojedyncza operacja |
| Niedelegowalne rekordy Power Apps | 500 domyślnie / 2000 maks. | lokalny limit przetwarzania |
| Get items w Power Automate | 100 domyślnie | domyślna liczba zwracanych elementów |

Dokumentacja:
- SharePoint Online limits: https://learn.microsoft.com/en-us/office365/servicedescriptions/sharepoint-online-service-description/sharepoint-online-limits
- Power Apps delegation: https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/delegation-overview
- SharePoint connector in Power Apps: https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/connections/connection-sharepoint-online
- Power Automate Get items guidance: https://learn.microsoft.com/en-us/sharepoint/dev/business-apps/power-automate/guidance/working-with-get-items-and-get-files

---

# 2. Pojemność listy a List View Threshold

SharePoint Online może przechowywać do 30 milionów elementów w liście lub 30 milionów plików i folderów w bibliotece.

Nie oznacza to jednak, że każde zapytanie może operować swobodnie na całym zbiorze.

List View Threshold wynosi:

```text
5 000 elementów
```

Jest to limit operacyjny dotyczący zapytań i widoków, a nie limit wielkości listy.

Przykład:

```text
Lista: 100 000 rekordów

Zapytanie:
- filtr po indeksowanej kolumnie
- wynik 300 rekordów
```

może działać poprawnie.

Natomiast:

```text
Lista: 100 000 rekordów

Zapytanie:
- brak selektywnego filtra
- sortowanie lub filtrowanie po niezindeksowanej kolumnie
- skan dużej części listy
```

może prowadzić do problemów z List View Threshold.

---

# 3. Indeksy

Przy większych listach należy świadomie projektować indeksy.

Dobre kandydaty to kolumny często używane do:

- filtrowania,
- sortowania,
- ograniczania zakresu danych,
- budowania widoków,
- zapytań Power Automate.

Przykład dla VCM:

```text
Status
Supplier
Created
Contract Number
Owner
```

Indeks powinien wynikać z rzeczywistych wzorców zapytań. Nie ma sensu indeksować wszystkich kolumn.

---

# 4. Delegacja w Power Apps

Power Apps próbuje delegować zapytania do źródła danych.

Przy zapytaniu delegowalnym:

```text
Power Apps
   |
   v
SharePoint wykonuje filtr
   |
   v
Power Apps pobiera wynik
```

Przy zapytaniu niedelegowalnym:

```text
Power Apps
   |
   v
pobiera ograniczony zbiór danych
   |
   v
filtruje lokalnie
```

Domyślny limit lokalnego przetwarzania wynosi 500 rekordów. Można go zwiększyć do 2000, ale nie zmienia to niedelegowalnego zapytania w delegowalne.

---

# 5. Delegacja a poprawność wyników

Problem delegacji dotyczy nie tylko wydajności.

Przykład:

```text
Lista: 100 000 rekordów
Szukany rekord: pozycja 35 000
Zapytanie: niedelegowalne
Limit lokalny: 500
```

Aplikacja może zwrócić:

```text
0 wyników
```

mimo że rekord istnieje.

Dlatego delegation warning może oznaczać niepełny lub błędny wynik.

---

# 6. Operacje niedelegowalne

Delegowalność zależy jednocześnie od:

- funkcji Power Fx,
- operatora,
- typu kolumny,
- źródła danych.

Szczególnej uwagi wymagają m.in.:

- `IsBlank`,
- `UpdateIf`,
- `RemoveIf`,
- niektóre operacje na polach Person,
- lookupy,
- złożone warunki,
- niektóre operacje na polu `ID`.

Nie należy zakładać, że sama funkcja `Filter()` jest zawsze delegowalna. Trzeba ocenić całe wyrażenie.

---

# 7. SharePoint ID

Pole `ID` jest polem systemowym i nie powinno być traktowane identycznie jak zwykła kolumna Number.

Typowy prosty filtr:

```powerfx
Filter(Contracts, ID = 123)
```

jest znacznie bezpieczniejszym przypadkiem niż budowanie złożonych zakresów i porównań po `ID`.

---

# 8. Pola Person / Group

Person / Group jest typem złożonym.

Typowe właściwości:

```text
DisplayName
Email
Claims
Department
JobTitle
```

Nie wszystkie operacje na tych właściwościach są delegowalne.

W zapytaniach należy jawnie określać właściwość, po której odbywa się porównanie, np. `Email` lub `DisplayName`, i weryfikować delegację konkretnego wyrażenia.

---

# 9. Lookup columns

Lookup jest wygodnym mechanizmem tworzenia zależności pomiędzy listami, ale duża liczba lookupów zwiększa złożoność zapytań.

Przykład:

```text
Contract
 -> Supplier
 -> Department
 -> Region
 -> Country
 -> Owner
 -> Manager
 -> Contract Type
 -> Currency
```

Im więcej zależności, tym trudniej utrzymać rozwiązanie pod względem wydajności, delegacji i diagnostyki.

---

# 10. Lookup threshold

SharePoint ma ograniczenia dotyczące liczby lookup/join operations w pojedynczym zapytaniu lub widoku.

W praktyce często spotykanym progiem jest około:

```text
12 lookup operations
```

Do kosztu lookupów mogą być zaliczane także niektóre pola systemowe oraz Person / Group.

Nie należy jednak projektować rozwiązania "pod limit". Jeśli model wymaga kilkunastu lookupów w jednym widoku, warto ponownie ocenić model danych.

---

# 11. Wielopoziomowe relacje

Głębokie zależności zwiększają złożoność zapytań.

Przykład:

```text
Contract
   |
Supplier
   |
Region
   |
Country
```

SharePoint nie jest dobrym zamiennikiem pełnego modelu relacyjnego w scenariuszach z dużą liczbą zależności i wielopoziomowych relacji.

---

# 12. Choice

Pole Choice nie jest zwykłym tekstem.

Typowy dostęp w Power Apps:

```powerfx
Status.Value
```

zamiast:

```powerfx
Status
```

Ma to znaczenie dla:

- `Filter`,
- `Patch`,
- ComboBox,
- porównań,
- migracji do Dataverse.

---

# 13. Lookup w Power Apps

Lookup jest rekordem złożonym.

Typowo dostępne są m.in.:

```text
Id
Value
```

Dlatego:

```powerfx
Supplier.Id
```

i:

```powerfx
Supplier.Value
```

oznaczają różne rzeczy.

---

# 14. Internal names kolumn

SharePoint przechowuje wewnętrzne nazwy kolumn niezależnie od późniejszej zmiany Display Name.

Przykład:

```text
Display Name:
Contract Number

Internal Name:
Contract_x0020_Number
```

Po zmianie Display Name internal name może pozostać bez zmian.

Ma to znaczenie dla:

- REST,
- OData,
- Filter Query,
- integracji,
- utrzymania Power Automate.

---

# 15. Get items w Power Automate

Akcja `Get items` nie powinna być traktowana jako mechanizm do pobierania całej dużej listy.

Domyślnie zwraca ograniczoną liczbę rekordów, typowo 100.

Przy większych zbiorach należy świadomie używać:

- Filter Query,
- Top Count,
- Pagination,
- indeksowanych kolumn.

---

# 16. Anti-pattern: Get everything + Apply to each

Nieefektywny wzorzec:

```text
Get items
↓
50 000 rekordów
↓
Apply to each
↓
Condition
↓
potrzebnych jest 8 rekordów
```

Lepszy wariant:

```text
Get items
Filter Query:
Status eq 'Submitted'
```

Filtrowanie powinno odbywać się możliwie blisko źródła danych.

---

# 17. Apply to each i liczba operacji

Przykład:

```text
Get 3000 items
↓
Apply to each
↓
Update item
```

oznacza około 3000 wywołań `Update item`, nie licząc pozostałych akcji.

Przy wielu równoległych flowach liczba operacji może bardzo szybko wzrosnąć.

---

# 18. Throttling

SharePoint Online i konektor SharePoint posiadają mechanizmy ochrony usługi.

Typowym objawem przekroczenia limitów jest:

```text
HTTP 429
Too Many Requests
```

Do throttlingu mogą prowadzić:

- intensywne pętle,
- wiele flowów używających tego samego connection,
- masowe aktualizacje elementów,
- częste odpytywanie dużych list,
- nadmierna równoległość.

Limity connectorów i usługi mogą się zmieniać, dlatego ich dokładne wartości należy zawsze sprawdzać w aktualnej dokumentacji Microsoft.

---

# 19. Trigger loops

Klasyczny problem:

```text
When item is modified
        |
        v
Update item
        |
        v
When item is modified
        |
       ...
```

Do ograniczenia takich sytuacji służą m.in.:

- Trigger Conditions,
- status guard,
- techniczne flagi,
- jawne przejścia stanu,
- przypisanie jednego właściciela modyfikacji statusu.

---

# 20. Race conditions

Jeżeli kilka flowów może modyfikować ten sam rekord, pojawia się ryzyko konkurencyjnych zapisów.

Przykład:

```text
Flow A czyta Contract
Flow B czyta Contract

Flow A zapisuje Status
Flow B zapisuje Status
```

Jeden proces może nadpisać wynik drugiego.

Dlatego stan biznesowy powinien mieć jasno określonego właściciela.

---

# 21. Brak klasycznej transakcyjności

SharePoint i Power Automate nie zapewniają klasycznej transakcji typu:

```text
BEGIN TRAN
COMMIT
ROLLBACK
```

Przykład:

```text
Update Contract   OK
Create Approval   OK
Update Supplier   FAIL
```

Wcześniejsze operacje nie zostaną automatycznie cofnięte.

W takich procesach trzeba projektować:

- retry,
- idempotency,
- recovery,
- compensating actions,
- jawny stan procesu.

---

# 22. State machine

SharePoint pozwala przechowywać kolumnę `Status`, ale sam nie gwarantuje poprawnych przejść pomiędzy stanami.

Przykład poprawnej sekwencji:

```text
Draft
  ↓
Submitted
  ↓
In Approval
  ↓
Approved
  ↓
Integrated
```

Bez dodatkowej logiki możliwa może być także niepoprawna zmiana:

```text
Draft -> Integrated
```

Reguły state machine muszą być kontrolowane przez aplikację, flow lub inną warstwę logiki.

---

# 23. Unique security scopes

SharePoint pozwala nadawać indywidualne uprawnienia elementom.

Każdy unikalny zestaw uprawnień może tworzyć osobny security scope.

Techniczny limit:

```text
50 000 unique security scopes
```

Przy dużych listach zalecana jest znacznie mniejsza liczba, często poniżej 5000.

Anti-pattern:

```text
Contract 1 -> unique permissions
Contract 2 -> unique permissions
Contract 3 -> unique permissions
...
```

Przy tysiącach rekordów taki model staje się trudny do utrzymania i może wpływać na wydajność.

---

# 24. Dziedziczenie uprawnień i 100 000 elementów

Przy dużych listach, bibliotekach lub folderach powyżej około 100 000 elementów pojawiają się dodatkowe ograniczenia związane z operacjami:

```text
break permission inheritance
restore permission inheritance
```

Nie jest to limit wielkości listy, tylko ograniczenie operacyjne związane z modelem zabezpieczeń.

---

# 25. Pliki i załączniki

Biblioteka dokumentów obsługuje znacznie większe pliki niż załączniki elementów listy.

```text
Pojedynczy plik w bibliotece: 250 GB
Załącznik do elementu listy: 250 MB
```

Jeżeli dokumenty są ważną częścią domeny, lepszym modelem jest zwykle:

```text
Document Library
+
metadata
+
powiązanie biznesowe
```

zamiast przechowywania ich jako attachments elementów listy.

---

# 26. Długość ścieżki

Pełna ścieżka pliku ma limit około:

```text
400 znaków
```

Głęboka struktura folderów może więc stać się problemem.

Przykład:

```text
Customers
 /2026
   /Europe
     /Poland
       /Division
         /Department
           /Contracts
```

W wielu scenariuszach lepszym rozwiązaniem jest używanie metadata zamiast bardzo głębokich struktur folderów.

---

# 27. Wersjonowanie

SharePoint obsługuje bardzo dużą liczbę wersji, ale nie oznacza to, że każda biblioteka powinna przechowywać ich maksymalną liczbę.

Duża liczba wersji:

- zwiększa zużycie storage,
- komplikuje lifecycle dokumentów,
- może nie mieć uzasadnienia biznesowego.

Polityka wersjonowania powinna być jawnie zaprojektowana.

---

# 28. Synchronizacja dużych bibliotek

Biblioteka może zawierać miliony plików, ale nie wszystkie powinny być synchronizowane na urządzenia użytkowników.

Dla dobrej wydajności OneDrive zalecana skala synchronizacji jest znacznie mniejsza i często podawana w okolicach:

```text
300 000 plików
```

To rekomendacja wydajnościowa, nie twardy limit pojemności biblioteki.

---

# 29. Szerokie listy

Problemy mogą wynikać nie tylko z liczby rekordów, ale również z liczby kolumn.

Przykład:

```text
Contract
100 kolumn
```

jeżeli aplikacja potrzebuje tylko kilku z nich.

Szeroki model zwiększa koszt transferu, renderowania i utrzymania.

---

# 30. Złożone typy pól

Szczególnej uwagi wymagają:

- Lookup,
- Person,
- Choice,
- Managed Metadata,
- Attachments,
- Calculated Columns.

Mogą:

- komplikować Power Fx,
- mieć ograniczenia delegacji,
- zwiększać koszt zapytań,
- utrudniać OData i integracje.

---

# 31. Rozproszona logika biznesowa

W rozwiązaniach SharePoint + Power Apps + Power Automate łatwo rozproszyć logikę biznesową pomiędzy:

```text
Canvas App
SharePoint validation
Flow A
Flow B
Flow C
```

Przykładowy skutek:

```text
kilka komponentów ustawia Contract.Status
```

Po pewnym czasie trudno ustalić, który komponent jest właścicielem danego stanu.

Dlatego warto jawnie definiować odpowiedzialności poszczególnych warstw.

---

# 32. "Ukryty system aplikacyjny"

Rozwiązanie może zacząć się od:

```text
1 lista
1 aplikacja
1 flow
```

a z czasem urosnąć do:

```text
30 list
10 aplikacji
50 flowów
dziesiątki lookupów
setki reguł
```

Technicznie nadal jest to SharePoint, ale architektonicznie jest to już rozbudowany system aplikacyjny.

W takim momencie warto ponownie ocenić, czy SharePoint nadal jest właściwym backendem.

---

# 33. Typowe anti-patterny Power Apps + SharePoint

## ClearCollect jako obejście delegacji

```powerfx
ClearCollect(colAll, BigList)
```

Nie naprawia delegacji. Przenosi problem do pamięci klienta.

## Lookup w każdym wierszu galerii

```text
Gallery 100 records
+
100 LookUp()
```

Może prowadzić do wzorca N+1.

## Ładowanie całej listy przy starcie

```text
App.OnStart
   |
   v
Load everything
```

pogarsza czas startu i skalowalność.

## Gigantyczny ekran

Duża liczba kontrolek, warunków `Visible` i logiki w `OnSelect` zwiększa sprzężenie aplikacji.

---

# 34. Typowe anti-patterny Power Automate + SharePoint

## Pobieranie wszystkiego

```text
Get items
↓
Apply to each
↓
Condition
```

zamiast filtrowania przy źródle.

## Modyfikacja elementu obserwowanego przez trigger

```text
When item modified
↓
Update same item
```

bez Trigger Conditions.

## Masowe Update item

Tysiące indywidualnych wywołań zwiększają ryzyko throttlingu.

## Wielu właścicieli statusu

Kilka flowów modyfikujących ten sam stan bez koordynacji zwiększa ryzyko race conditions.

## Retry każdego błędu

Retry powinien wynikać z klasy błędu i charakteru operacji.

---

# 35. Dobre praktyki

Przy używaniu SharePoint jako backendu warto:

1. Projektować indeksy przed znacznym wzrostem danych.
2. Filtrować dane przy źródle.
3. Pilnować delegation warnings.
4. Nie używać kolekcji jako obejścia delegacji.
5. Ograniczać liczbę lookupów.
6. Ograniczać unique permissions.
7. Używać Trigger Conditions.
8. Unikać pełnych `Get items` bez potrzeby.
9. Projektować jawny state machine.
10. Monitorować throttling i HTTP 429.
11. Ustalić właściciela zmian statusu.
12. Testować aplikację na realistycznym wolumenie danych.
13. Używać bibliotek dokumentów do dokumentów.
14. Ograniczać głębokość struktur folderów.
15. Rozdzielać stan biznesowy od stanu technicznego.

---

# 36. Kiedy SharePoint jest dobrym backendem

SharePoint jest dobrym wyborem dla rozwiązań takich jak:

- proste formularze,
- niewielkie aplikacje CRUD,
- ewidencje,
- lekkie workflow,
- rozwiązania dokumentowe,
- aplikacje z niewielką liczbą relacji,
- rozwiązania z prostym modelem bezpieczeństwa.

Przykłady:

```text
rejestr wyposażenia
prosta lista zgłoszeń
ewidencja dokumentów
mały workflow akceptacyjny
rejestr umów o umiarkowanej złożoności
```

---

# 37. Kiedy rozważyć Dataverse

Dataverse warto rozważyć, gdy jednocześnie pojawia się kilka z poniższych cech:

- duża liczba relacji,
- wiele lookupów,
- granularny model security,
- wiele ról biznesowych,
- auditing,
- złożony state machine,
- wiele automatyzacji,
- integracje z systemami zewnętrznymi,
- wiele aplikacji korzystających z tego samego modelu,
- DEV / TEST / PROD,
- wymagania ALM,
- potrzeba jednoznacznego modelu domenowego.

Decyzja nie powinna wynikać z jednego limitu, np. przekroczenia 5000 elementów.

---

# 38. Najważniejsze liczby do zapamiętania

```text
30 000 000
= pojemność listy / biblioteki

5 000
= List View Threshold

500 / 2000
= lokalny limit niedelegowalnego Power Apps

50 000
= maksymalna liczba unique security scopes

100
= domyślna liczba wyników Get items
```

Każda z tych wartości opisuje inną warstwę systemu.

---

# 39. Podsumowanie

SharePoint Online może być skutecznym backendem dla Power Apps i Power Automate, jeśli rozwiązanie jest projektowane z uwzględnieniem jego modelu danych i limitów operacyjnych.

Najważniejsze rozróżnienie:

> **Limit pojemności mówi, ile danych SharePoint może przechować. Limity operacyjne mówią, jak można z tymi danymi pracować.**

SharePoint nie przestaje działać przy 5001 rekordach.

Problemy pojawiają się wtedy, gdy rosną jednocześnie:

```text
wolumen
+
liczba relacji
+
złożoność security
+
liczba flowów
+
liczba operacji
+
złożoność stanu biznesowego
```

Jeżeli coraz więcej logiki i mechanizmów służy jedynie do obchodzenia ograniczeń źródła danych, warto ponownie ocenić wybór backendu.
