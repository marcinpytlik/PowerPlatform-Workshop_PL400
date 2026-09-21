# SharePoint Online jako backend dla Power Apps i Power Automate

## Cel materiału

Ten dokument opisuje ograniczenia i ryzyka SharePoint Online w kontekście budowania aplikacji Power Apps oraz automatyzacji Power Automate.

Najważniejszy wniosek:

> SharePoint może przechowywać bardzo dużo danych. To nie znaczy, że każdy sposób pracy z tymi danymi będzie dobrze skalowalny.

Nie należy sprowadzać tematu do zdania:

> "SharePoint ma limit 5000 rekordów."

To nieprawda.

Trzeba rozdzielić:

- pojemność listy lub biblioteki,
- limity widoków i zapytań,
- delegację Power Apps,
- sposób pobierania danych przez Power Automate,
- lookupy,
- bezpieczeństwo,
- throttling,
- model relacji,
- architekturę procesu.

---

# 1. Najważniejsze liczby

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
| Zalecana skala synchronizacji | ok. 300 000 plików | soft limit OneDrive sync |
| Cross-site move/copy | 30 000 plików / 100 GB | pojedyncza operacja |
| Niedelegowalne rekordy Power Apps | 500 domyślnie / 2000 maks. | lokalny limit przetwarzania |
| Get items w Power Automate | 100 domyślnie | trzeba świadomie ustawiać filtr/paginację |

Dokumentacja:
- SharePoint Online limits: https://learn.microsoft.com/en-us/office365/servicedescriptions/sharepoint-online-service-description/sharepoint-online-limits
- Power Apps delegation: https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/delegation-overview
- SharePoint connector and delegation: https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/connections/connection-sharepoint-online
- Power Automate Get items guidance: https://learn.microsoft.com/en-us/sharepoint/dev/business-apps/power-automate/guidance/working-with-get-items-and-get-files

---

# 2. 30 milionów elementów nie oznacza "bez limitów"

SharePoint Online może przechowywać do:

```text
30 000 000 elementów w liście
30 000 000 plików i folderów w bibliotece
```

To jest limit pojemności.

Nie należy go mylić z:

```text
5 000 = List View Threshold
```

Lista z 100 000 rekordów może działać poprawnie.

Problem pojawia się wtedy, gdy zapytanie próbuje przetwarzać zbyt duży zakres danych bez odpowiedniego filtrowania i indeksów.

---

# 3. List View Threshold – 5000

List View Threshold wynosi:

```text
5 000
```

To nie jest maksymalna liczba rekordów w liście.

To próg operacyjny związany z kosztownymi zapytaniami i widokami.

Typowy problem:

```text
Contracts
100 000 rekordów

widok / zapytanie
bez indeksu
bez selektywnego filtra
```

Może prowadzić do błędów lub ograniczeń przetwarzania.

## Dobra praktyka

Projektuj:

- indeksowane kolumny,
- selektywne filtry,
- widoki zwracające ograniczony zbiór danych.

---

# 4. Indeksy

Indeksy powinny być projektowane zanim lista stanie się duża.

Dobre kandydaty w VCM:

```text
Status
Supplier
Created
Contract Number
Owner
```

Nie indeksuj wszystkiego bez potrzeby.

Pytanie projektowe:

> Po jakich kolumnach aplikacja i flow najczęściej filtrują dane?

---

# 5. Power Apps – delegacja

Power Apps próbuje wykonać zapytanie po stronie SharePoint.

Jeżeli zapytanie jest delegowalne:

```text
Power Apps
   |
Filter(...)
   |
SharePoint filtruje
   |
Power Apps dostaje wynik
```

Jeżeli nie:

```text
Power Apps
   |
pobiera lokalny fragment
   |
filtruje lokalnie
```

Domyślny limit niedelegowalnego przetwarzania:

```text
500 rekordów
```

Maksymalny konfigurowalny:

```text
2000 rekordów
```

To nie naprawia delegacji.

---

# 6. Delegacja jest problemem poprawności, nie tylko wydajności

Przykład:

```text
Lista = 100 000 rekordów
Szukany Contract = rekord 35 000
Zapytanie = niedelegowalne
Limit lokalny = 500
```

Aplikacja może zwrócić:

```text
0 wyników
```

mimo że rekord istnieje.

Najważniejsze zdanie:

> Delegation warning może oznaczać błędny wynik, a nie tylko wolniejszą aplikację.

---

# 7. Nie wszystkie operacje Power Fx delegują do SharePoint

Delegowalność zależy od:

- źródła danych,
- typu pola,
- użytej funkcji,
- operatora.

Szczególnej uwagi wymagają:

- `IsBlank`,
- `UpdateIf`,
- `RemoveIf`,
- pola Person,
- Lookup,
- złożone warunki,
- operacje na ID.

Nie ucz uczestników reguły:

> "Filter zawsze deleguje."

Poprawna reguła:

> Trzeba sprawdzić, czy konkretna formuła jest delegowalna dla konkretnego źródła.

---

# 8. SharePoint ID

Pole `ID` jest specjalnym polem systemowym.

Typowy bezpieczny przypadek:

```text
ID = 123
```

Nie zakładaj, że wszystkie operatory porównania działają tak samo jak na zwykłej kolumnie liczbowej.

---

# 9. Person / Group

Person / Group jest strukturą złożoną.

Może zawierać:

```text
DisplayName
Email
Claims
Department
JobTitle
```

Nie wszystkie operacje na tych właściwościach delegują się jednakowo.

W praktyce najlepiej jawnie wiedzieć, po czym filtrujemy:

```text
Email
DisplayName
```

i sprawdzić delegację konkretnego wyrażenia.

---

# 10. Lookup columns

Lookupi są wygodne, ale duża liczba lookupów komplikuje zapytania.

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

W takim momencie warto już zadać pytanie:

> Czy SharePoint nadal jest właściwym modelem danych?

---

# 11. Lookup threshold

SharePoint ma ograniczenia dotyczące liczby lookup/join operations w pojedynczym zapytaniu.

W praktyce często spotykana wartość:

```text
12 lookup operations
```

Do tego kosztu mogą dokładać się nie tylko klasyczne lookupy, ale również np. pola Person/Group.

Nie traktuj jednak liczby 12 jako celu projektowego.

Jeśli rozwiązanie zbliża się do kilkunastu lookupów w jednym widoku lub zapytaniu, ważniejsze jest pytanie architektoniczne niż próba "zmieszczenia się w limicie".

---

# 12. Wielopoziomowe relacje

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

SharePoint nie jest systemem, w którym warto bez ograniczeń budować głęboki graf relacji.

Im więcej relacji i lookup expansion, tym większa złożoność zapytań oraz ryzyko problemów z delegacją.

---

# 13. Choice nie jest zwykłym tekstem

Pole SharePoint Choice w Power Apps jest strukturą.

Typowy dostęp:

```powerfx
Status.Value
```

a nie:

```powerfx
Status
```

To ma znaczenie przy:

- filtrowaniu,
- Patch,
- porównaniach,
- migracji do Dataverse.

---

# 14. Lookup nie jest zwykłym tekstem

Lookup może udostępniać m.in.:

```text
Id
Value
```

Dlatego:

```powerfx
Supplier.Value
```

i:

```powerfx
Supplier.Id
```

to nie to samo.

---

# 15. Internal names kolumn

Kolumna utworzona jako:

```text
Contract Number
```

może mieć internal name:

```text
Contract_x0020_Number
```

Późniejsza zmiana Display Name nie musi zmienić internal name.

To ma znaczenie szczególnie dla:

- REST,
- OData,
- Power Automate Filter Query,
- integracji,
- utrzymania solution.

---

# 16. Power Automate – Get items

Domyślnie `Get items` zwraca ograniczoną liczbę elementów.

Typowa wartość domyślna:

```text
100
```

Nie należy zakładać:

> "Get items pobierze całą listę."

Dla większych zestawów trzeba świadomie projektować:

- Filter Query,
- Top Count,
- Pagination,
- indeksy.

---

# 17. Anti-pattern: Get everything + Apply to each

Źle:

```text
Get items
↓
50 000 rekordów
↓
Apply to each
↓
Condition
↓
potrzebujemy 8 rekordów
```

Lepiej:

```text
Get items
Filter Query:
Status eq 'Submitted'
```

Filtruj przy źródle.

---

# 18. Apply to each może zwielokrotnić liczbę operacji

Przykład:

```text
Get 3000 items
↓
Apply to each
↓
Update item
```

to około:

```text
3000 Update item
```

plus pozostałe akcje.

Funkcjonalnie może działać.

Architektonicznie może bardzo źle skalować się wraz ze wzrostem danych i liczby flowów.

---

# 19. Throttling

SharePoint Online i konektor SharePoint mają mechanizmy ochrony usługi.

Objaw:

```text
HTTP 429
Too Many Requests
```

Źródłem może być:

- wiele flowów,
- wspólne connection,
- tysiące akcji w pętli,
- równoległe przetwarzanie,
- intensywne odpytywanie list.

Ważne:

> Limit connectora może dotyczyć współdzielonego connection, nie tylko jednego flow.

Dokładne wartości limitów mogą się zmieniać, dlatego przed szkoleniem warto sprawdzić aktualną dokumentację Microsoft.

---

# 20. Trigger loops

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

Rozwiązania:

- Trigger Conditions,
- status guard,
- techniczne flagi,
- jasne ownership statusu,
- świadome przejścia state machine.

---

# 21. Race conditions i lost updates

Przykład:

```text
Flow A czyta Contract
Flow B czyta Contract

Flow A zapisuje Status
Flow B zapisuje Status
```

Wynik zależy od kolejności zapisów.

Jeżeli kilka flowów może zmieniać ten sam stan, projekt zaczyna być trudny do kontrolowania.

Pytanie architektoniczne:

> Kto jest właścicielem zmiany tego statusu?

---

# 22. Brak transakcyjności

SharePoint + Power Automate nie daje klasycznego:

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

Pierwsze operacje nie zostaną automatycznie cofnięte.

Trzeba projektować:

- recovery,
- retry,
- idempotency,
- compensating action,
- jawny stan procesu.

---

# 23. SharePoint nie pilnuje pełnego state machine

Możemy mieć statusy:

```text
Draft
Submitted
In Approval
Approved
Integrated
```

ale SharePoint sam w sobie nie gwarantuje:

```text
Draft -> Submitted -> In Approval -> Approved
```

Jeżeli aplikacja lub flow źle zapisze status, technicznie może powstać:

```text
Draft -> Integrated
```

Reguły procesu muszą być kontrolowane przez aplikację / automatyzację.

---

# 24. Unique security scopes

Techniczny limit:

```text
50 000 unique security scopes
```

Rekomendacja projektowa:

```text
utrzymuj znacząco mniej,
często jako punkt odniesienia < 5000
```

Anti-pattern:

```text
Contract 1 -> unique permissions
Contract 2 -> unique permissions
Contract 3 -> unique permissions
...
```

Przy tysiącach rekordów model bezpieczeństwa szybko staje się kosztowny.

---

# 25. 100 000 elementów a permission inheritance

Przy bardzo dużych listach i bibliotekach pojawiają się dodatkowe ograniczenia operacji:

```text
break inheritance
restore inheritance
```

na poziomie większych kontenerów.

Warto o tym pamiętać szczególnie przy modelach, które próbują używać SharePoint jako systemu row-level security.

---

# 26. Pliki i załączniki

Biblioteka dokumentów:

```text
pojedynczy plik do 250 GB
```

Załącznik do elementu listy:

```text
do 250 MB
```

Jeżeli dokumenty są ważnym elementem domeny:

```text
Document Library
+
metadata
+
powiązanie biznesowe
```

jest zwykle lepszym modelem niż duża liczba załączników listowych.

---

# 27. Długość ścieżki

Maksymalna pełna ścieżka:

```text
400 znaków
```

Głęboka hierarchia:

```text
Customers
 /2026
   /Europe
     /Poland
       /Division
         /Department
           /Contracts
```

może stać się problemem.

Dlatego w SharePoint często lepiej używać:

```text
metadata
```

zamiast próbować modelować wszystko folderami.

---

# 28. Versioning

Limity mogą być bardzo wysokie, ale duża liczba wersji:

- zużywa storage,
- komplikuje lifecycle dokumentu,
- nie zawsze ma wartość biznesową.

Polityka wersjonowania powinna być świadoma.

---

# 29. Synchronizacja dużych bibliotek

Biblioteka może zawierać miliony dokumentów.

To nie oznacza, że wszystkie powinny być synchronizowane przez OneDrive na komputer użytkownika.

Dla najlepszej wydajności Microsoft rekomenduje znacznie mniejszą skalę synchronizacji, często około:

```text
300 000 plików
```

---

# 30. Szerokie listy

Problemy powoduje nie tylko liczba rekordów.

Przykład:

```text
Contract
100 kolumn
```

Jeżeli aplikacja potrzebuje tylko:

```text
8 kolumn
```

warto ograniczać zakres danych i projektować model świadomie.

---

# 31. Złożone typy pól

Szczególnej uwagi wymagają:

```text
Lookup
Person
Choice
Managed Metadata
Attachments
Calculated columns
```

Nie dlatego, że są złe.

Dlatego, że:

- mają złożoną strukturę,
- mogą mieć ograniczenia delegacji,
- komplikują Power Fx i OData,
- zwiększają koszt zapytań.

---

# 32. Rozproszona logika biznesowa

Typowa ewolucja:

```text
Canvas OnSelect
+
SharePoint validation
+
Flow A Condition
+
Flow B
+
Flow C
```

Po pewnym czasie pojawia się pytanie:

> Kto właściwie ustawia status Contract?

To jest ważny sygnał architektoniczny.

---

# 33. "Ukryta baza aplikacyjna"

Projekt może zacząć się od:

```text
1 lista
1 Power App
1 flow
```

a po roku mieć:

```text
30 list
10 aplikacji
50 flowów
dziesiątki lookupów
setki reguł
```

Technicznie nadal jest to SharePoint.

Architektonicznie powstał duży system aplikacyjny bez jawnej warstwy domenowej.

---

# 34. Kiedy SharePoint jest dobrym backendem

Dobry kandydat:

- prosta aplikacja,
- mało relacji,
- prosty model uprawnień,
- umiarkowany wolumen,
- niewielka liczba automatyzacji,
- brak złożonego state machine,
- dokumenty są ważną częścią rozwiązania.

Przykłady:

- rejestr wyposażenia,
- prosta lista zgłoszeń,
- mała ewidencja,
- prosty workflow akceptacyjny,
- rozwiązanie dokumentowe.

---

# 35. Kiedy rozważyć Dataverse

Sygnały:

- dużo relacji,
- dużo lookupów,
- wiele ról,
- granular security,
- auditing,
- rozbudowany state machine,
- dużo automatyzacji,
- integracje,
- DEV / TEST / PROD,
- ALM,
- wiele aplikacji korzystających z tego samego modelu.

Nie jeden sygnał sam w sobie.

Raczej kombinacja wielu z nich.

---

# 36. Power Apps + SharePoint – anti-patterny

## 1. ClearCollect jako "naprawa" delegacji

```powerfx
ClearCollect(colAll, BigList)
```

## 2. Lookup w każdym wierszu galerii

```text
Gallery 100 rows
+
100 LookUp()
```

## 3. Jeden ogromny ekran i cała logika w OnSelect

## 4. Dziesiątki lookupów

## 5. Ładowanie całej listy w App.OnStart

---

# 37. Power Automate + SharePoint – anti-patterny

## 1.

```text
Get items ALL
↓
Apply to each
↓
Condition
```

## 2.

```text
When item modified
↓
Update same item
```

bez trigger guard.

## 3.

Tysiące indywidualnych `Update item`.

## 4.

Kilka flowów zmieniających ten sam status.

## 5.

Retry każdego błędu bez klasyfikacji.

---

# 38. Dobre praktyki

Jeżeli świadomie wybieramy SharePoint:

1. Projektuj indeksy wcześnie.
2. Filtruj po stronie źródła.
3. Pilnuj delegation warnings.
4. Nie używaj kolekcji jako obejścia delegacji.
5. Minimalizuj liczbę lookupów.
6. Minimalizuj unique permissions.
7. Używaj Trigger Conditions.
8. Nie pobieraj całych list bez potrzeby.
9. Projektuj state machine.
10. Monitoruj throttling.
11. Ustal właściciela statusu.
12. Testuj na realistycznym wolumenie danych.
13. Używaj bibliotek dokumentów do dokumentów.
14. Nie buduj całej taksonomii folderami.

---

# 39. Pięć liczb, które warto pokazać uczestnikom

```text
30 000 000
= pojemność listy / biblioteki

5 000
= List View Threshold

500 / 2000
= niedelegowalne rekordy Power Apps

50 000
= max unique security scopes

100
= domyślna liczba wyników Get items
```

Te wartości opisują różne warstwy systemu.

Nie należy ich mieszać.

---

# 40. Pytanie kontrolne dla grupy

Zapytaj:

> Która z tych liczb mówi, ile rekordów może mieć aplikacja Power Apps?

Poprawna odpowiedź:

> Żadna sama w sobie.

Liczy się kombinacja:

```text
wolumen
+
delegacja
+
indeksy
+
filtry
+
lookupy
+
security
+
Power Automate
+
sposób użycia danych
```

---

# 41. Jak wykorzystać to w VCM

Po LAB 01:

> Na pięciu Contracts wszystko działa idealnie.

Potem:

> A co przy 100 000 Contracts?

> A co przy 15 lookupach?

> A co przy osobnych permissions dla każdej umowy?

> A co przy pięciu flowach zmieniających Status?

> A co przy historii Approval?

Nie mów:

> SharePoint się do tego nie nadaje.

Powiedz:

> Wraz ze wzrostem wymagań koszt utrzymania modelu SharePoint zaczyna rosnąć.

To naturalnie prowadzi do LAB 05 i Dataverse.

---

# 42. Najważniejsze zdania na slajd

> **SharePoint nie przestaje działać przy 5001 rekordach. Problem zaczyna się wtedy, gdy aplikacja zachowuje się tak, jakby danych było zawsze pięć.**

> **Delegation warning nie zawsze oznacza wolniejszą aplikację. Czasami oznacza błędną odpowiedź.**

> **Limit pojemności mówi, ile danych SharePoint może przechować. Limity operacyjne mówią, jak możesz z tymi danymi pracować.**

> **Jeżeli coraz więcej energii poświęcamy na obchodzenie ograniczeń źródła zamiast na rozwój procesu biznesowego, warto ponownie ocenić wybór platformy.**

---

# 43. Krótki talk track prowadzącego

Po LAB 01 nie rób wykładu o wszystkich limitach.

Pokaż tylko:

```text
30 mln != 5000
```

i powiedz:

> SharePoint może mieć bardzo dużą listę. Problemem nie jest sama liczba rekordów, tylko sposób, w jaki później próbujemy je filtrować, łączyć i zabezpieczać.

Po LAB 02 dodaj:

```text
500 / 2000
```

i wyjaśnij delegację.

Po LAB 03 dodaj:

```text
trigger loop
race conditions
```

Po LAB 11 wróć do:

```text
Get everything
vs
Filter at source
```

Wtedy ograniczenia SharePoint tworzą jedną historię zamiast jednego długiego wykładu.

---

# 44. Wniosek architektoniczny

Migracja VCM do Dataverse nie jest wykonywana dlatego, że:

```text
SharePoint przekroczył 5000 rekordów
```

Migrujemy dlatego, że rozwiązanie zaczyna wymagać:

```text
silniejszego modelu relacyjnego
jawnego state machine
auditingu
lepszego modelu security
procesowej obserwowalności
ALM
wspólnego modelu dla wielu aplikacji
```

To jest argument architektoniczny, a nie "ucieczka od limitu 5000".
