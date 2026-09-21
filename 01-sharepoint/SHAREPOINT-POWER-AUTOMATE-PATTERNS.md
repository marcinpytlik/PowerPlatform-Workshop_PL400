# SharePoint Online + Power Automate – wzorce i pułapki

## Cel dokumentu

Dokument opisuje praktyczne wzorce używania Power Automate z listami i bibliotekami SharePoint Online.

## 1. Triggery

Najczęściej używane triggery to:

- When an item is created,
- When an item is created or modified,
- When a file is created,
- When a file is created or modified.

Dobór triggera powinien wynikać z procesu, a nie z wygody.

## 2. Trigger Conditions

Trigger Conditions ograniczają uruchamianie procesu przed utworzeniem runu.

Przykład:

```text
Status = Submitted
```

jest lepszym guardem niż uruchamianie flow przy każdej zmianie i kończenie go na pierwszym Condition.

## 3. Trigger loop

Klasyczny problem:

```text
When item is modified
        |
        v
Update item
        |
        v
When item is modified
```

Rozwiązania:

- Trigger Conditions,
- status guard,
- techniczne flagi,
- jasny state machine,
- ograniczenie właścicieli statusu.

## 4. Get changes for an item or a file

Akcja może być używana do określania, które właściwości zmieniły się pomiędzy wersjami.

Typowe zastosowanie:

```text
czy zmienił się Status?
czy zmienił się Owner?
czy zmienił się Amount?
```

Wymaga świadomie skonfigurowanego versioningu.

## 5. Zmiana metadata vs zawartość pliku

Zmiana właściwości elementu i zmiana zawartości pliku to różne zdarzenia.

Przy projektowaniu flowów dokumentowych trzeba jawnie określić, które z nich mają uruchamiać proces.

## 6. Get items

Nie należy pobierać całej listy, jeśli potrzebny jest mały podzbiór.

Preferowany model:

```text
Filter Query
+
Top Count
+
Pagination jeśli potrzebna
```

## 7. OData Filter Query

Przykład:

```text
Status eq 'Submitted'
```

Filtr powinien być wykonywany po stronie SharePoint.

## 8. Apply to each

`Apply to each` nie jest problemem samym w sobie.

Problem pojawia się, gdy iteruje po tysiącach elementów, które można było odfiltrować wcześniej.

## 9. Concurrency

Równoległość może przyspieszyć niezależne operacje, ale może też powodować:

- throttling,
- race conditions,
- konflikty zapisu,
- trudniejszą diagnostykę.

## 10. Wiele flowów modyfikujących ten sam rekord

Jeżeli wiele flowów zmienia ten sam `Status`, powstaje niejawny distributed state machine.

Lepiej określić jednego właściciela przejść stanu lub jawnego orchestratora.

## 11. Retry

Retry powinien być stosowany świadomie.

Nie należy automatycznie ponawiać każdego błędu.

Szczególnej uwagi wymagają operacje tworzące dane i potencjalne duplikaty.

## 12. Correlation ID

Procesy wieloetapowe powinny mieć własny identyfikator korelacyjny.

```text
Business ID
+ Correlation ID
+ Flow Run ID
```

pozwala odtworzyć pełny timeline.

## 13. Brak transakcyjności

SharePoint + Power Automate nie zapewniają klasycznego rollbacku wielu operacji.

Dlatego trzeba projektować:

- retry,
- idempotency,
- recovery,
- compensating actions,
- statusy pośrednie.

## 14. Run History

Run History dobrze pokazuje konkretny run.

Nie wystarcza jako jedyne źródło diagnostyki dla procesu rozłożonego na kilka flowów.

## 15. Anti-patterny

- Get all + Apply to each + Condition.
- Trigger na każdą zmianę bez guardu.
- Update same item bez kontroli trigger loop.
- Wiele flowów zmieniających jeden status.
- Retry każdego błędu.
- Brak correlation ID.

## 16. Dokumentacja

- https://learn.microsoft.com/en-us/sharepoint/dev/business-apps/power-automate/sharepoint-connector-actions-triggers
- https://learn.microsoft.com/en-us/sharepoint/dev/business-apps/power-automate/guidance/working-with-get-items-and-get-files
