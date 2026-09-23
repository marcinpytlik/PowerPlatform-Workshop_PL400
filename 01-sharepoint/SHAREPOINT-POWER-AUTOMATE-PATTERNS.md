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


## 21. Retry Policy w akcji HTTP – konfiguracja krok po kroku

Retry Policy służy do ponawiania akcji po błędach przejściowych, takich jak chwilowa niedostępność usługi, timeout lub throttling.

Microsoft zaleca stosowanie retry dla błędów transient, a nie dla błędów biznesowych.

### Gdzie ustawić Retry Policy

1. Otwórz flow w Power Automate.
2. Zaznacz akcję `HTTP`.
3. Otwórz panel `Settings`.
4. Znajdź sekcję `Retry Policy`.
5. Wybierz odpowiedni typ polityki.

Dostępne typy zależą od akcji, ale typowo są to:

```text
Default
None
Fixed Interval
Exponential Interval
```

### Default

Jeżeli nie ustawisz własnej polityki, akcja korzysta z polityki domyślnej connectora/runtime.

Domyślna polityka dla wielu operacji ma charakter exponential retry.

Nie należy zakładać konkretnego interwału bez sprawdzenia aktualnej dokumentacji i zachowania konkretnej akcji.

### None

```text
Retry Policy = None
```

oznacza brak automatycznego ponawiania.

Używaj, gdy ponowienie nie ma sensu albo może spowodować niepożądane skutki.

Przykłady:

- 400 Bad Request,
- 409 Conflict wynikający z reguły biznesowej,
- błąd walidacji,
- operacja nieidempotentna, której nie wolno powtórzyć bez dodatkowej kontroli.

### Fixed Interval

Przykład:

```text
Retry Policy: Fixed Interval
Count: 3
Interval: PT10S
```

oznacza maksymalnie trzy ponowienia co 10 sekund.

Format czasu używa ISO 8601 Duration:

```text
PT5S  = 5 sekund
PT30S = 30 sekund
PT2M  = 2 minuty
```

Fixed Interval jest prosty i przewidywalny, ale przy dużej liczbie klientów może generować zsynchronizowane ponowienia.

### Exponential Interval

Exponential retry zwiększa odstęp między kolejnymi próbami i jest preferowany dla wielu błędów przejściowych.

Przykład konfiguracyjny:

```text
Retry Policy: Exponential Interval
Count: 3
Minimum interval: PT5S
Maximum interval: PT30S
```

Dokładne pola widoczne w designerze mogą zależeć od akcji i wersji interfejsu.

### Dobór retry do kodu HTTP

Praktyczna zasada:

| HTTP | Typ błędu | Retry |
|---|---|---|
| 200/201/204 | sukces | nie |
| 400 | request niepoprawny | nie |
| 401/403 | auth/permissions | zwykle nie |
| 404 | brak zasobu | zwykle nie |
| 409 | konflikt biznesowy / duplikat | zwykle nie |
| 408 | timeout | często tak |
| 429 | throttling | tak |
| 500 | błąd serwera | zależnie od operacji |
| 502/503/504 | błąd przejściowy infrastruktury | często tak |

### Retry i idempotencja

Retry jest bezpieczne tylko wtedy, gdy ponowienie tej samej operacji nie powoduje niekontrolowanych skutków ubocznych.

Przykład ryzyka:

```text
POST create contract
-> timeout
-> klient nie wie, czy rekord został utworzony
-> retry
-> możliwy duplikat
```

Dlatego dla operacji tworzących dane należy stosować:

- business key,
- idempotency key,
- correlation ID,
- kontrolę duplikatów,
- właściwą interpretację 409.

### Przykład dla VCM Mock API

```text
VCM/LAB04/201 -> bez retry
VCM/LAB04/409 -> None
VCM/LAB04/429 -> Exponential Interval
VCM/LAB04/500 -> test obu wariantów
VCM/LAB04/SLOW -> retry zależnie od celu ćwiczenia
```

Dla demonstracji throttlingu można ustawić:

```text
Retry Policy: Exponential Interval
Count: 3
Minimum interval: PT5S
Maximum interval: PT30S
```

Następnie w Run History sprawdzić:

- liczbę prób,
- czas pomiędzy próbami,
- status końcowy,
- correlation ID,
- tracked properties.

### Retry Policy nie zastępuje error handling

Nawet poprawnie ustawiony retry nie zwalnia z obsługi końcowego błędu.

Typowy wzorzec:

```text
HTTP
  |
  +--> sukces -> dalszy proces
  |
  +--> po wyczerpaniu retry -> CATCH / log / status Integration Error
```

### Dokumentacja

- https://learn.microsoft.com/en-us/power-automate/guidance/coding-guidelines/error-handling
- https://learn.microsoft.com/en-us/azure/logic-apps/error-exception-handling
