# Kiedy SharePoint przestaje być dobrym backendem dla Canvas App

## Cel

SharePoint Online jest dobrym backendem dla wielu prostych i średnio złożonych aplikacji biznesowych. Nie jest jednak uniwersalnym zamiennikiem relacyjnej bazy danych ani platformy transakcyjnej.

Dokument opisuje sygnały, że należy rozważyć Dataverse, SQL lub API.

## 1. Rosnąca liczba relacji

Jeżeli model zaczyna przypominać:

```text
A 1:N B
B N:N C
C 1:N D
D N:1 E
```

i aplikacja wykonuje wiele lookupów między listami, SharePoint zaczyna generować koszt złożoności.

## 2. Integralność danych

SharePoint nie daje takich samych mechanizmów jak relacyjna baza danych dla:

- constraints,
- transactions,
- foreign keys,
- cascade behavior.

Jeżeli integralność jest krytyczna, logika aplikacyjna może nie wystarczyć.

## 3. Transakcyjność

Proces:

```text
zapis A
zapis B
zapis C
albo rollback wszystkiego
```

nie jest naturalnym scenariuszem SharePoint + Power Automate.

## 4. Intensywna współbieżność

Jeżeli wielu użytkowników jednocześnie edytuje te same rekordy i wymagane są silne gwarancje optimistic concurrency, warto rozważyć backend lepiej dostosowany do tego problemu.

## 5. Bardzo złożony security model

Sygnały:

- tysiące unikalnych permission scopes,
- łamanie inheritance per item,
- wiele wyjątków,
- security zależne od pól rekordu,
- rozbudowane role biznesowe.

Dataverse może zapewnić bardziej naturalny model security.

## 6. Złożony workflow

Jeżeli status rekordu ma dziesiątki przejść, wiele równoległych ścieżek i kompensacje, sam SharePoint nie powinien być właścicielem całej logiki procesu.

## 7. Delegation zaczyna sterować UX

Jeżeli projekt UI jest ciągle kompromisem wynikającym z non-delegable queries, oznacza to niedopasowanie backendu do sposobu dostępu.

## 8. Raportowanie

Jeżeli wymagane są:

- złożone joiny,
- agregacje,
- historia zmian jako dane analityczne,
- duże przekroje,

SharePoint może być niewygodnym źródłem.

## 9. Integracje

Jeżeli wiele systemów zewnętrznych zapisuje dane równolegle, rozważ API jako kontrolowaną warstwę dostępu zamiast bezpośredniego dostępu do list.

## 10. Dane krytyczne

Jeżeli proces wymaga:

- wysokich gwarancji spójności,
- ścisłego audytu,
- recovery,
- jednoznacznej kontroli zmian,
- rozbudowanej kontroli dostępu,

wybór backendu powinien zostać ponownie oceniony.

## 11. Sygnały ostrzegawcze

```text
dużo list
+ dużo lookupów
+ dużo flowów
+ dużo item-level permissions
+ dużo wyjątków
+ dużo kolekcji w Canvas
+ częste problemy z delegacją
+ trudne deploymenty
```

to nie jest pojedynczy problem. To sygnał architektoniczny.

## 12. Alternatywy

### Dataverse

Dobre dopasowanie, gdy rozwiązanie jest mocno osadzone w Power Platform i wymaga:

- relacji,
- security roles,
- audytu,
- business rules,
- model-driven app,
- ALM.

### SQL

Dobre dopasowanie dla relacyjnych danych i złożonych zapytań, gdy organizacja posiada odpowiednią warstwę bezpieczeństwa i integracji.

### API

Dobre, gdy chcemy:

- ukryć backend,
- centralizować reguły biznesowe,
- zapewnić kontrolowany kontrakt,
- obsługiwać wielu klientów.

## 13. Strangler pattern

Migracja nie musi być jednorazowa.

Można:

```text
SharePoint prototype
-> nowy moduł w Dataverse/API
-> stopniowe przełączanie funkcji
-> migracja danych
```

## 14. Zasada

Nie pytaj tylko:

```text
Czy da się to zrobić w SharePoint?
```

Pytaj:

```text
Czy SharePoint pozostanie najprostszym i najbardziej przewidywalnym backendem po wzroście rozwiązania?
```
