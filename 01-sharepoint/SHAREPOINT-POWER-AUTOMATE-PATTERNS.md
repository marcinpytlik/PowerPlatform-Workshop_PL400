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


## 17. Partial update elementu SharePoint przez HTTP

Standardowa akcja `Update item` w Power Automate może wymagać uzupełnienia wielu pól oznaczonych w SharePoint jako wymagane. Jeżeli celem jest zmiana tylko jednej lub kilku kolumn istniejącego elementu, można użyć akcji:

```text
SharePoint -> Send an HTTP request to SharePoint
```

Przykład: zmiana wyłącznie kolumny `Status` na `In Approval`.

### Konfiguracja akcji

Method:

```text
POST
```

Uri:

```text
_api/web/lists/GetByTitle('Contracts')/items(<ID>)
```

Przykład z dynamicznym ID:

```text
_api/web/lists/GetByTitle('Contracts')/items(@{triggerBody()?['ID']})
```

Headers:

```text
Accept: application/json;odata=nometadata
Content-Type: application/json;odata=nometadata
IF-MATCH: *
X-HTTP-Method: MERGE
```

Body:

```json
{
  "Status": "In Approval"
}
```

Efekt:

```text
Title        -> bez zmian
Supplier     -> bez zmian
Amount       -> bez zmian
ValidFrom    -> bez zmian
ValidTo      -> bez zmian
Status       -> In Approval
```

Jest to odpowiednik aktualizacji tylko wskazanej kolumny, np. koncepcyjnie:

```sql
UPDATE Contracts
SET Status = 'In Approval'
WHERE ID = <ID>;
```

### Ważne uwagi

- używana jest wewnętrzna nazwa kolumny SharePoint,
- dla kolumn prostych body może zawierać tylko zmieniane pola,
- Lookup, Person, Managed Metadata i niektóre typy złożone wymagają właściwego formatu REST,
- `IF-MATCH: *` oznacza aktualizację bez sprawdzania konkretnej wersji ETag,
- jeśli ważna jest kontrola współbieżności, należy użyć rzeczywistego ETag zamiast `*`,
- partial update nie powoduje ponownego zastosowania wartości domyślnych do pozostałych pól,
- operacja nadal może uruchomić flow reagujące na modyfikację tego elementu.

### Kiedy użyć

`Update item` jest czytelniejsze dla prostych scenariuszy i powinno być pierwszym wyborem, gdy mapowanie pól nie jest problemem.

`Send an HTTP request to SharePoint` jest przydatne, gdy:

- lista ma wiele wymaganych pól,
- trzeba zmienić tylko niewielką część rekordu,
- nie chcemy przepisywać wartości wszystkich wymaganych kolumn,
- potrzebna jest większa kontrola nad requestem REST.

## 18. Dokumentacja HTTP SharePoint

- https://learn.microsoft.com/en-us/sharepoint/dev/business-apps/power-automate/guidance/working-with-send-sp-http-request
- https://learn.microsoft.com/en-us/sharepoint/dev/sp-add-ins/complete-basic-operations-using-sharepoint-rest-endpoints


## 19. Bezpośrednie uruchamianie flow z Canvas App

Jeżeli użytkownik zapisuje rekord w Canvas App i proces biznesowy ma rozpocząć się od razu, można uruchomić flow bezpośrednio z aplikacji zamiast czekać na trigger SharePoint.

Nie używa się wtedy triggera:

```text
Manually trigger a flow
```

tylko triggera:

```text
Power Apps (V2)
```

Jest to nadal flow typu instant cloud flow, ale jego wywołującym jest Canvas App.

Schemat:

```text
Canvas App
    |
    | Flow.Run(...)
    v
Power Automate
    |
    +--> walidacja
    +--> Get item / Update item
    +--> Approval
    +--> HTTP / API
```

### Przykład

Flow ma trigger `Power Apps (V2)` i parametr wejściowy:

```text
ContractId - Number
```

Po dodaniu flow do aplikacji można go wywołać z Power Fx:

```powerfx
VCM_SubmitContract.Run(
    ThisItem.ID
)
```

Jeżeli aplikacja najpierw zapisuje dane do SharePoint:

```powerfx
Patch(
    Contracts,
    ThisItem,
    {
        Status: { Value: "Submitted" }
    }
);

VCM_SubmitContract.Run(
    ThisItem.ID
)
```

Alternatywnie flow może być właścicielem zmiany statusu:

```powerfx
VCM_SubmitContract.Run(
    ThisItem.ID
)
```

a po stronie Power Automate:

```text
Power Apps (V2)
    |
    v
Get item
    |
    v
sprawdzenie aktualnego stanu
    |
    v
Update Status = Submitted / In Approval
    |
    v
dalszy proces
```

Drugi wariant zmniejsza zależność od tego, czy SharePoint zdążył uruchomić trigger zdarzeniowy.

### Porównanie

```text
Canvas App -> SharePoint update -> SharePoint trigger
```

zalety:

- luźniejsze powiązanie aplikacji z flow,
- proces może reagować również na zmiany wykonane poza aplikacją.

wady:

- start flow nie jest bezpośrednio kontrolowany przez aplikację,
- może wystąpić opóźnienie pomiędzy zmianą listy a rozpoczęciem runu.

```text
Canvas App -> Flow.Run(...)
```

zalety:

- wywołanie flow następuje bezpośrednio po akcji użytkownika,
- aplikacja może przekazać parametry,
- prostsze sterowanie komendami typu Submit / Retry / Cancel.

wady:

- Canvas App jest zależna od konkretnego flow,
- flow musi walidować parametry przekazane przez klienta.

### Bezpieczeństwo

Parametr przekazany z Canvas App nie powinien być traktowany jako dowód uprawnienia.

Przykład:

```text
action = APPROVE
```

nie powinno samo w sobie oznaczać, że użytkownik ma prawo zatwierdzić kontrakt.

Flow powinien sprawdzić:

- użytkownika wywołującego,
- bieżący status rekordu,
- wymagane role lub reguły biznesowe,
- czy przejście stanu jest dozwolone.

## 20. Dokumentacja Power Apps -> Power Automate

- https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/how-to/trigger-flow
