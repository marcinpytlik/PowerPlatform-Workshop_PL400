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
Update Status = InApproval
        |
        v
Finance required?
        |
        +-- Amount <= 100000 ------> Legal Approval
        |
        +-- Amount > 100000 -------> Finance Approval -> Legal Approval
        |
        +-- Amount > 500000 -------> Management Approval
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
- Status: `InApproval`,
- pozostałe wymagane pola zmapuj z triggera.

> to Update ponownie spełni trigger „created or modified”. Drugi run powinien zakończyć się, ponieważ Status nie jest już `Submitted`. W LAB 09 wykorzystamy tę sytuację do diagnostyki.

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

2. Wyślij email do RequestorEmail:

```text
Subject: Contract <ContractNumber> approved
```

3. Treść zawiera:
   - dostawcę,
   - kwotę,
   - CorrelationId.

---

# Zadanie 10 – Testy

## Test A – 50 000

Oczekiwane:

```text
Legal only -> Approved
```

## Test B – 150 000

Oczekiwane:

```text
Finance -> Legal -> Approved
```

## Test C – 650 000

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

# Materiał Microsoft

- SharePoint triggers: https://learn.microsoft.com/en-us/sharepoint/dev/business-apps/power-automate/sharepoint-connector-actions-triggers
- Create and test an approval workflow: https://learn.microsoft.com/en-us/power-automate/modern-approvals
