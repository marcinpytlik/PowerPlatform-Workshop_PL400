# LAB 03 – Power Automate: pierwszy proces akceptacji

## Cel laboratorium

Zbudować automatyczny proces akceptacji umowy uruchamiany po utworzeniu lub zmianie rekordu SharePoint.

Po laboratorium uczestnik potrafi:

- utworzyć automated cloud flow,
- skonfigurować trigger SharePoint,
- ograniczyć niepotrzebne uruchomienia flow,
- pobrać dane powiązane,
- uruchomić Approval,
- rozgałęzić proces na podstawie wyniku,
- zapisać status do SharePoint,
- rozpoznać ryzyko pętli trigger -> update -> trigger.

## Czas

90 minut.

## Wymagania

LAB 01 i LAB 02.

---

# Docelowy przebieg

```text
When item is created or modified
        |
        v
czy Status = Submitted?
        |
        v
Generate CorrelationId
        |
        v
Update Status = In Approval
        |
        v
ścieżka wg Amount (bez przeliczenia waluty)
        |
        +-- Amount <= 100000 ---------------------> Legal
        |
        +-- Amount > 100000 i <= 500000 -----------> Finance -> Legal
        |
        +-- Amount > 500000 -----------------------> Finance -> Legal -> Management
        |
        v
Approved / Rejected
        |
        v
Update Contract
        |
        v
Notification
```

---

# Zadanie 1 – Utworzenie flow

1. Otwórz `https://make.powerautomate.com`.
2. Wybierz właściwe środowisko.
3. **Create -> Automated cloud flow**.
4. Nazwa:

```text
VCM - Contract Submitted - SP
```

5. Trigger:

```text
SharePoint - When an item is created or modified
```

6. Ustaw:
   - Site Address: witryna szkoleniowa,
   - List Name: `Contracts`.

> Trigger SharePoint jest event-driven, ale nie należy traktować go jak synchronicznego wywołania aplikacyjnego. Między zapisem elementu a rozpoczęciem flow może wystąpić opóźnienie. Jeżeli aplikacja ma świadomie uruchamiać proces natychmiast po akcji użytkownika, alternatywą jest flow typu instant z triggerem `Power Apps (V2)` wywoływany z Canvas App przez `.Run(...)`. W tym LAB pozostajemy przy triggerze SharePoint, żeby najpierw poznać model event-driven.

---

# Zadanie 2 – Ograniczenie uruchomień

Nie chcemy wykonywać procesu przy każdej zmianie rekordu.

Najprostszy wariant szkoleniowy:

1. Dodaj Condition bezpośrednio po triggerze.
2. Warunek:

```text
Status Value equals Submitted
```

3. Gałąź `No` zakończ akcją `Terminate` ze statusem `Succeeded` i komunikatem:

```text
Contract is not in Submitted state. Nothing to do.
```

Gałąź `No` kończymy statusem `Succeeded`, a nie `Failed`, ponieważ brak stanu `Submitted` oznacza kontrolowane pominięcie pracy, a nie błąd techniczny.

## Wariant zaawansowany – Trigger Conditions

Otwórz trigger -> **Settings** i dodaj Trigger Condition odpowiadający polu Status. Ze względu na techniczną nazwę kolumny i format payloadu najlepiej zbudować wyrażenie na podstawie rzeczywistego outputu triggera w Twoim tenantcie.

Cel dyskusji:

- Condition uruchamia flow i dopiero potem kończy wykonanie,
- Trigger Condition może zapobiec utworzeniu niepotrzebnego runu.

---

# Zadanie 3 – Correlation ID

Dodaj akcję **Compose** o nazwie `Compose - CorrelationId`.

Expression:

```text
guid()
```

Dodaj `Update item` dla Contracts:

- ID: ID z triggera,
- CorrelationId: output Compose,
- Status: `In Approval`,
- pozostałe wymagane pola zmapuj z triggera.

> Standardowa akcja `Update item` może wymagać ponownego zmapowania kolumn oznaczonych w SharePoint jako Required. Wartości domyślne listy nie są mechanizmem automatycznego „dopisywania” brakujących pól podczas aktualizacji istniejącego rekordu.

Jeżeli lista ma wiele wymaganych pól, alternatywą jest częściowa aktualizacja przez:

```text
SharePoint -> Send an HTTP request to SharePoint
```

Przykład zmiany tylko statusu:

```text
POST
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

Na tym etapie LAB użyj `Update item`, a wariant partial update potraktuj jako rozszerzenie.

> To Update ponownie spełni trigger „created or modified”. Drugi run powinien zakończyć się, ponieważ Status nie jest już `Submitted`. W LAB 10 wykorzystamy tę sytuację do diagnostyki.

---

# Zadanie 4 – Pobranie dostawcy

Dodaj `Get item` dla listy `Suppliers`.

- ID: ID z pola Lookup Supplier dostarczonego przez Contracts.

Nadaj nazwę akcji:

```text
Get Supplier
```

Później użyjemy danych dostawcy w treści Approval.

---

# Zadanie 5 – Finansowa ścieżka akceptacji

Dodaj Condition:

```text
Amount > 100000
```

W gałęzi Yes utwórz rekord `ContractApprovals`:

- Contract: bieżąca umowa,
- ApprovalType: Finance,
- ApproverEmail: adres uczestnika/prowadzącego,
- Status: Pending.

Następnie dodaj:

```text
Approvals - Start and wait for an approval
```

Approval type:

```text
Approve/Reject - First to respond
```

Title:

```text
Finance approval - <ContractNumber>
```

Details powinny zawierać:

```text
Supplier: <SupplierName>
Amount: <Amount> <Currency>
Valid to: <ValidTo>
Correlation ID: <CorrelationId>
```

Assigned to: testowy adres approvera.

---

# Zadanie 6 – Obsługa decyzji

Po Approval dodaj Condition:

```text
Outcome equals Approve
```

## Approve

1. Zaktualizuj rekord ContractApprovals:
   - Status = Approved,
   - DecisionDate = `utcNow()`,
   - Comment = komentarz z Approval.
2. Przejdź dalej.

## Reject

1. Zaktualizuj ContractApprovals:
   - Status = Rejected,
   - DecisionDate = `utcNow()`.
2. Update Contract:
   - Status = Rejected.
3. Wyślij email do RequestorEmail.
4. `Terminate` ze statusem `Succeeded` – proces zakończył się biznesowym odrzuceniem, a nie błędem technicznym.

---

# Zadanie 7 – Legal Approval

Po zakończeniu Finance lub bezpośrednio dla kwoty <=100000 dodaj analogiczny etap `Legal`.

W praktyce najprościej podczas szkolenia:

- Finance jest warunkowe,
- Legal jest zawsze wymagane.

Utwórz rekord `ContractApprovals` i Start and wait for an approval.

Po odrzuceniu -> Contract `Rejected`.

Po akceptacji -> przejdź dalej.

---

# Zadanie 8 – Management Approval

Dodaj warunek:

```text
Amount > 500000
```

Jeżeli Yes, dodaj trzeci Approval typu `Management`.

Na tym etapie możesz skopiować logikę z Finance i zmienić typ oraz approvera.

> Cel dydaktyczny: po wykonaniu flow zapytamy, czy kopiowanie całych bloków jest właściwą architekturą. W dalszych laboratoriach zrefaktoryzujemy proces.

---

# Zadanie 9 – Finalizacja

Po wszystkich wymaganych Approval:

1. Update Contract:

```text
Status = Approved
```

2. W LAB 04, przed rozpoczęciem wywołania zewnętrznego API, ustawimy dodatkowo `Integration Pending`. Dzięki temu stan biznesowej akceptacji i stan integracji są rozróżnione.

3. Wyślij email do RequestorEmail:

```text
Subject: Contract <ContractNumber> approved
```

4. Treść zawiera:
   - dostawcę,
   - kwotę,
   - CorrelationId.

---

# Zadanie 10 – Testy

Progi są liczbowe, bez FX. `VCM/2026/002` ma 150 000 EUR i i tak idzie w Finance.

## Test A – 50 000 PLN

Nowa umowa albo `VCM/2026/001` ustawione na `Submitted`.

Oczekiwane:

```text
Legal only -> Approved
```

## Test B – 150 000

`VCM/2026/002` (EUR w danych testowych).

Oczekiwane:

```text
Finance -> Legal -> Approved
```

## Test C – 650 000 PLN

`VCM/2026/003`.

Oczekiwane:

```text
Finance -> Legal -> Management -> Approved
```

## Test D – odrzucenie Finance

Oczekiwane:

```text
Rejected
```

oraz brak kolejnych Approval.

---

# Analiza Run History

Po wykonaniu testów:

1. Otwórz flow.
2. Przejdź do **Run history**.
3. Otwórz run dla testu B.
4. Rozwiń trigger.
5. Porównaj:
   - Inputs,
   - Outputs.
6. Otwórz `Update item`.
7. Sprawdź czas wykonania.
8. Otwórz Approval.
9. Znajdź Output zawierający decyzję.
10. Zapisz Flow Run ID z adresu URL lub dostępnego kontekstu.

---

# Kryterium ukończenia

- flow uruchamia się dla Submitted,
- kwota steruje wymaganymi Approval,
- odrzucenie kończy proces biznesowo,
- status końcowy jest zapisany w Contracts,
- Approval history znajduje się w ContractApprovals,
- uczestnik potrafi znaleźć konkretny run.

## Po tym LAB

Talk track: **Trigger Guard**, Single Responsibility, correlation ID. Drugi run po `Update` zostaw na LAB 10 – dziś tylko go zauważ.

---

# Challenge

Zamiast powielać trzy bloki Approval zaprojektuj konfigurację:

```text
ApprovalType | MinimumAmount | Approver
Legal        | 0             | legal@...
Finance      | 100000        | finance@...
Management   | 500000        | management@...
```

Nie implementuj jeszcze. Narysuj rozwiązanie i zastanów się, czy konfiguracja powinna być przechowywana w SharePoint, Dataverse czy Environment Variables.

---

# Alternatywa: bezpośrednie wywołanie flow z Canvas App

Jeżeli scenariusz wymaga, aby użytkownik po kliknięciu `Submit` uruchamiał proces bez czekania na SharePoint trigger, utwórz osobny instant cloud flow z triggerem:

```text
Power Apps (V2)
```

i parametrem wejściowym np.:

```text
ContractId
```

Wywołanie z Power Fx:

```powerfx
VCM_SubmitContract.Run(ThisItem.ID)
```

Flow powinien po swojej stronie ponownie pobrać rekord i zweryfikować stan oraz uprawnienia. Parametr z klienta nie jest dowodem autoryzacji.

---

# Materiał Microsoft

- SharePoint triggers: https://learn.microsoft.com/en-us/sharepoint/dev/business-apps/power-automate/sharepoint-connector-actions-triggers
- Create and test an approval workflow: https://learn.microsoft.com/en-us/power-automate/modern-approvals
