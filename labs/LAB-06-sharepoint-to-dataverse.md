# LAB 06 – Migracja rozwiązania SharePoint -> Dataverse

## Cel laboratorium

Przenieść działający prototyp z LAB 01–04 na model Dataverse z LAB 05. Po tym LAB-ie **Canvas App oraz główny proces Power Automate pracują na Dataverse**, a SharePoint pozostaje jedynie punktem odniesienia do porównania architektury.

Po ukończeniu uczestnik potrafi:

- przenieść dane testowe ze SharePoint do Dataverse,
- przepiąć Canvas App na tabele Dataverse,
- dostosować Power Fx do nowego modelu danych,
- zastąpić trigger SharePoint triggerem Dataverse,
- zastąpić akcje SharePoint akcjami Dataverse,
- poprawnie mapować lookupy i Choices,
- wykonać test regresyjny po migracji.

## Czas

90–120 minut.

## Wymagania

- ukończone LAB 01–05,
- Solution `Vendor Contract Management`,
- tabele `Supplier`, `Contract`, `Approval`, `Process Log`,
- działający Canvas App `VCM - Contract Portal`,
- działający prototyp flow z LAB 03–04.

---

# Stan przed migracją

```text
Canvas App
   |
   v
SharePoint
   |
   v
Power Automate
   |
   +--> Approvals
   +--> HTTP/API
```

# Stan po migracji

```text
Canvas App
   |
   v
Dataverse
   |
   v
Power Automate Orchestrator
   |
   +--> Approval
   +--> API Integration
   +--> Process Log
```

---

# Zadanie 1 – Punkt kontrolny przed zmianą

Przed przepięciem rozwiązania:

1. uruchom Canvas App,
2. otwórz istniejącą umowę,
3. utwórz nową umowę,
4. uruchom proces dla statusu `Submitted`,
5. zapisz wynik testu jako baseline.

Nie usuwaj jeszcze list SharePoint ani starego flow.

---

# Zadanie 2 – Migracja danych testowych

Przenieś minimum:

- 3 Suppliers,
- 5 Contracts,
- powiązane Approval history, jeśli jest potrzebne do dalszych ćwiczeń.

Możesz użyć importu, Dataflows, Power Automate lub ręcznego wprowadzenia dla małego zestawu szkoleniowego.

## Reguły mapowania

| SharePoint | Dataverse |
|---|---|
| Suppliers.Title | Supplier.Name |
| SupplierCode | Supplier Code |
| Contracts.Title | Contract Number |
| Supplier Lookup | Supplier Lookup |
| Amount | Amount |
| Currency | Currency Code |
| ValidFrom | Valid From |
| ValidTo | Valid To |
| Status | Status |
| CorrelationId | Correlation ID |
| ExternalSystemId | External System ID |

Po migracji sprawdź alternate keys i relacje.

---

# Zadanie 3 – Dodanie tabel Dataverse do Canvas App

W `VCM - Contract Portal`:

1. dodaj źródła Dataverse:
   - Contracts,
   - Suppliers,
   - Approvals,
2. **nie usuwaj jeszcze źródeł SharePoint**,
3. przepinaj ekran po ekranie,
4. po każdym ekranie wykonuj Preview.

Cel: unikamy jednorazowej zmiany całej aplikacji bez możliwości znalezienia miejsca regresji.

---

# Zadanie 4 – Galeria Contracts

Zmień `Items` galerii tak, aby korzystała z tabeli Dataverse `Contract`.

Zwróć uwagę na różnice:

- primary name nie jest już SharePoint `Title`,
- Lookup Supplier jest rekordem Dataverse,
- Choice Status jest wartością Choice,
- nazwy wyświetlane i schema names to różne pojęcia.

Nie kopiuj ślepo formuły SharePoint. Odtwórz jej intencję:

```text
status filter
AND
StartsWith(Contract Number, search text)
```

Sprawdź delegation warning.

---

# Zadanie 5 – Formularze

Przepnij:

- `frmContractDetails`,
- `frmContract`

na tabelę Dataverse `Contract`.

Sprawdź:

- Supplier Lookup,
- Amount,
- Currency Code,
- Valid From,
- Valid To,
- Status,
- External System ID,
- Correlation ID.

W `OnSuccess` nie używaj już `LastSubmit.Title`. Po przepięciu formularza na Dataverse primary name tabeli Contract to `Contract Number`.

Dla naszego modelu ustaw np.:

```powerfx
Notify(
    "Umowa została zapisana",
    NotificationType.Success
);

Trace(
    "Contract saved",
    TraceSeverity.Information,
    {
        ContractNumber: frmContract.LastSubmit.'Contract Number'
    }
);

Navigate(
    scrContracts,
    ScreenTransition.Fade
)
```

Jeżeli Power Apps podkreśla:

```powerfx
frmContract.LastSubmit.Title
```

to jest to pozostałość po modelu SharePoint z LAB 02. Po migracji do Dataverse należy odwoływać się do kolumny Dataverse:

```powerfx
frmContract.LastSubmit.'Contract Number'
```

Apostrofy są wymagane, ponieważ display name kolumny zawiera spację. Jeżeli w aplikacji używasz innej nazwy wyświetlanej, wybierz właściwość rekordu podpowiadaną przez IntelliSense.

---

# Zadanie 6 – Requestor

W SharePoint używaliśmy `RequestorEmail` jako tekstu.

W Dataverse mamy Lookup do User.

Omów dwa warianty:

1. Requestor jako Lookup -> User,
2. dodatkowe pole tekstowe z adresem email tylko wtedy, gdy istnieje uzasadniona potrzeba integracyjna.

Dostosuj aplikację i flow do wybranego modelu.

---

# Zadanie 7 – Nowy trigger Dataverse

Utwórz w Solution nowy flow:

```text
VCM - Contract Submitted
```

Trigger:

```text
Microsoft Dataverse - When a row is added, modified or deleted
```

Ustaw:

- Change type: Added, Modified,
- Table name: Contract,
- Scope: Organization lub zgodnie z wymaganiami szkolenia.

Dodaj warunek/trigger condition tak, aby logika biznesowa rozpoczynała się wyłącznie dla `Submitted`.

> Starego flow SharePoint jeszcze nie usuwaj. Wyłącz je po pozytywnym teście nowego procesu.

---

# Zadanie 8 – Zastąpienie akcji SharePoint

Zastąp:

```text
Get item      -> Get a row by ID
Update item   -> Update a row
Create item   -> Add a new row
```

Dotyczy to przede wszystkim:

- Contract,
- Supplier,
- Approval.

Przy lookupach używaj identyfikatorów rekordów Dataverse, a nie nazw tekstowych.

---

# Zadanie 9 – Status i Correlation ID

Po wejściu w proces:

1. wygeneruj `guid()`,
2. zapisz Correlation ID,
3. ustaw:

```text
Status = In Approval
```

Po pełnej akceptacji:

```text
Status = Approved
```

Przed wywołaniem API:

```text
Status = Integration Pending
```

Po HTTP 201:

```text
Status = Integrated
```

Błąd techniczny będzie później kończył się:

```text
Status = Integration Error
```

---

# Zadanie 10 – Approval history w Dataverse

Zamiast `ContractApprovals` SharePoint użyj tabeli `Approval`.

Każdy etap akceptacji powinien tworzyć osobny rekord:

```text
Contract
Approval Type
Approver
Status
Decision Date
Comment
```

Nie przechowuj całej historii tylko w Run History Power Automate.

---

# Zadanie 11 – Wyłączenie starego procesu

Po pozytywnych testach:

1. wyłącz `VCM - Contract Submitted - SP`,
2. pozostaw go tymczasowo jako materiał porównawczy,
3. upewnij się, że ta sama zmiana biznesowa nie uruchamia dwóch procesów.

---

# Zadanie 12 – Test regresyjny

Wykonaj:

## Test A – Canvas App

- lista umów działa,
- wyszukiwanie działa,
- filtr statusu działa,
- można utworzyć i edytować Contract,
- Supplier Lookup działa.

Progi jak w LAB 03: surowe `Amount`, bez FX.

## Test B – 50 000 PLN

```text
Submitted -> In Approval -> Legal -> Approved
```

## Test C – 150 000

Liczbowo powyżej 100 000, niezależnie od waluty.

```text
Submitted -> Finance -> Legal -> Approved
```

## Test D – API

```text
Approved -> Integration Pending -> Integrated
```

Sprawdź, że dane zmieniają się w Dataverse, a nie w SharePoint.

---

# Zadanie 13 – Docelowy podział odpowiedzialności

Po migracji narysuj docelowy kierunek refaktoryzacji:

```text
VCM - Contract Submitted
        |
        v
Orchestrator
   |
   +--> VCM - Approval
   +--> VCM - API Integration
   +--> VCM - Notification
   +--> Process Log / Error Handler
```

Nie musisz jeszcze rozdzielać wszystkich flowów. Zrobimy to przed finalnym pakowaniem Solution.

---

# Kryterium ukończenia

- Canvas App korzysta z Dataverse,
- nowy Contract jest zapisywany w Dataverse,
- główny flow używa triggera Dataverse,
- akcje biznesowe nie korzystają już z list SharePoint,
- Approval history trafia do tabeli Approval,
- statusy są zgodne ze wspólnym modelem,
- stare flow SharePoint jest wyłączone,
- test regresyjny przechodzi.

## Po tym LAB

To był **Strangler Migration Pattern**: nowy model obok starego, przepięcie po komponencie, regresja, dopiero wyłączenie SharePoint flow.

---

# Materiał Microsoft

- Dataverse connector: https://learn.microsoft.com/en-us/connectors/commondataserviceforapps/
- Create a canvas app with Dataverse: https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/data-platform-create-app
- Dataverse triggers in Power Automate: https://learn.microsoft.com/en-us/power-automate/dataverse/create-update-delete-trigger
