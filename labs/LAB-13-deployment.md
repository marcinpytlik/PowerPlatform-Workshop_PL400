# LAB 13 – Deployment DEV -> TEST: managed solution i smoke test

## Wariant na sali (60 min)

W agendzie 3-dniowej nie każdy robi pełne E2E.

| Kto | Zadania |
|---|---|
| Wszyscy | 1–9: freeze, kontrola, export managed, import, connections, env vars, włączenie flowów |
| Wszyscy | 10–11: smoke Model-driven + Canvas |
| Prowadzący na rzutniku | 12–13: E2E 150 000 i negative test 500 |
| Jeśli jest czas | 14–15: managed layers i Pipelines |

Uczestnik kończy LAB, gdy managed `1.0.0.0` jest w TEST, `VCM_API_BASE_URL` nie wskazuje hard-code DEV i smoke przechodzi.

## Cel laboratorium

Przeprowadzić kontrolowany deployment rozwiązania Vendor Contract Management z DEV do TEST i wykonać test po wdrożeniu.

## Czas

90–120 minut.

## Wymagania

- dwa środowiska: DEV i TEST,
- Dataverse w obu środowiskach,
- ukończony LAB 12,
- wymagane connections utworzone lub możliwe do utworzenia w TEST.

---

# Docelowy przepływ

```text
DEV
Unmanaged
   |
   | export managed
   v
Artifact 1.0.0.0
   |
   v
TEST
Managed
   |
   +-- environment variables
   +-- connection references
   +-- enable flows
   +-- smoke test
   +-- E2E test
```

---

# Faza 1 – Pre-deployment check w DEV

## Zadanie 1 – Freeze wersji

Przed eksportem nie wprowadzaj kolejnych zmian funkcjonalnych.

W Solution ustaw:

```text
Version = 1.0.0.0
```

Zapisz datę i osobę wykonującą deployment.

---

# Zadanie 2 – Kontrola komponentów

Zweryfikuj checklistę:

- [ ] Tables są w Solution
- [ ] Choices są w Solution
- [ ] Canvas App jest w Solution
- [ ] Model-driven App jest w Solution
- [ ] Flows są w Solution
- [ ] Connection References istnieją
- [ ] Environment Variables istnieją
- [ ] API URL nie jest hard-coded
- [ ] support email nie jest hard-coded
- [ ] wszystkie zmiany zostały zapisane i opublikowane
- [ ] flowy w DEV przechodzą test podstawowy

---

# Zadanie 3 – Dependencies

Sprawdź dependencies Solution.

Jeżeli system wskazuje missing required components:

1. nie eksportuj „na siłę”,
2. dodaj brakujące komponenty,
3. ponownie wykonaj kontrolę.

---

# Faza 2 – Eksport

# Zadanie 4 – Export as managed

W DEV:

1. Otwórz Solution.
2. Wybierz Export.
3. Wykonaj publish changes, jeżeli system tego wymaga/rekomenduje.
4. Uruchom checker, jeżeli dostępny.
5. Wybierz wariant:

```text
Managed
```

6. Eksportuj plik.

Zapisz nazwę artefaktu, np.:

```text
VendorContractManagement_1_0_0_0_managed.zip
```

Nie rozpakowuj i nie edytuj ręcznie artefaktu przed importem.

---

# Faza 3 – Import do TEST

# Zadanie 5 – Przełączenie środowiska

1. W Power Apps przełącz Environment na TEST.
2. Potwierdź nazwę środowiska przed importem.
3. Otwórz Solutions.

Prowadzący powinien celowo zadać pytanie:

> Skąd wiem, że naprawdę jestem w TEST?

Nie opieraj się wyłącznie na kolorze UI. W produkcyjnych procesach stosuj jasne nazwy środowisk i governance.

---

# Zadanie 6 – Import

1. **Import solution**.
2. Wskaż managed ZIP.
3. Przejdź przez ekran importu.
4. Skonfiguruj wymagane Connection References.
5. Ustaw Environment Variables:

Przykład:

```text
VCM_API_BASE_URL = https://api-test.example/...
VCM_SUPPORT_EMAIL = powerplatform-test@example.com
VCM_DEFAULT_CURRENCY = PLN
VCM_ENABLE_EXTERNAL_INTEGRATION = true
```

6. Rozpocznij import.
7. Po zakończeniu przejrzyj wynik importu.

Jeśli import kończy się błędem, nie próbuj ponownie w ciemno. Otwórz szczegóły i znajdź pierwszy istotny komunikat.

---

# Zadanie 7 – Connection References

Po imporcie sprawdź:

- Dataverse connection,
- Outlook connection,
- Approvals connection,
- SharePoint connection – jeśli Solution nadal go używa,
- connector do API/custom connector.

Każdy connection reference powinien wskazywać połączenie właściwe dla TEST.

---

# Zadanie 8 – Environment Variables

Otwórz Solution i sprawdź wartości.

Szczególnie zweryfikuj:

```text
VCM_API_BASE_URL
```

Nie może wskazywać DEV.

To jest punkt kontrolny typu **stop deployment**, jeżeli wartość jest błędna.

---

# Zadanie 9 – Flow activation

Sprawdź każdy flow.

Jeżeli flow jest Off:

1. otwórz flow,
2. sprawdź connections,
3. sprawdź missing references,
4. dopiero potem Turn on.

Nie włączaj masowo flowów, jeśli nie wiesz, czy target configuration jest poprawna.

---

# Faza 4 – Smoke test

# Zadanie 10 – Model-driven App

1. Uruchom `VCM - Contract Administration`.
2. Otwórz Suppliers.
3. Utwórz Supplier:

```text
TEST Supplier
SUP-TEST-001
```

4. Utwórz Contract:

```text
VCM/TEST/001
Amount = 50000
Status = Draft
```

5. Zapisz.

Jeżeli nie można utworzyć rekordu, sprawdź:

- security role,
- app access,
- table permissions.

---

# Zadanie 11 – Canvas App

1. Uruchom `VCM - Contract Portal`.
2. Sprawdź listę Contract.
3. Utwórz nową umowę.
4. Sprawdź, czy zapis trafia do Dataverse/źródła oczekiwanego w wersji końcowej.

---

# Zadanie 12 – E2E

Utwórz:

```text
ContractNumber = VCM/TEST/002
Amount = 150000
Status = Submitted
```

Oczekiwany proces:

```text
Submitted
-> Finance Approval
-> Legal Approval
-> Approved
-> API TEST
-> Integrated
```

Wykonaj Approval.

Sprawdź:

- Contract Status,
- Approval rows,
- External System ID,
- Correlation ID,
- Process Logs.

---

# Zadanie 13 – Negative test

Utwórz umowę powodującą błąd API 500 lub użyj przełącznika mock API.

Oczekiwane:

```text
Contract = Integration Error
ProcessLog = Error
notification -> TEST support
flow run = Failed
```

Sprawdź, czy powiadomienie nie trafiło do produkcyjnej grupy wsparcia.

---

# Faza 5 – Dokumentacja wdrożenia

Uzupełnij:

```text
Solution: Vendor Contract Management
Version: 1.0.0.0
Source: DEV
Target: TEST
Deployment date:
Deployed by:
Managed: Yes
API URL:
Support email:
Connection references checked: Yes/No
Smoke test: PASS/FAIL
E2E test: PASS/FAIL
Negative test: PASS/FAIL
Known issues:
```

---

# Zadanie 14 – Managed solution behavior

W TEST spróbuj wejść do komponentu i omów, jakie zmiany są możliwe oraz jak działają managed layers.

Pytanie:

> Czy poprawkę do TEST robimy ręcznie w TEST czy w DEV i ponownie wdrażamy Solution?

Docelowa odpowiedź:

```text
Zmiana źródłowa powstaje w DEV, jest wersjonowana i wdrażana kontrolowanym procesem.
```

---

# Zadanie 15 – Pipeline – demonstracja / rozszerzenie

Jeżeli środowisko ma skonfigurowane Power Platform Pipelines:

1. pokaż deployment stage DEV -> TEST,
2. wybierz Solution,
3. uruchom deployment,
4. pokaż konfigurację environment variables i connections,
5. porównaj z ręcznym export/import.

Microsoft Power Platform Pipelines wdrażają rozwiązania oraz konfigurację target environment, w tym connections, connection references i environment variables. Nie przenoszą jednak danych zapisanych w tabelach Dataverse jako części Solution.

---

# Kryterium ukończenia

LAB jest ukończony, gdy:

- Solution 1.0.0.0 jest zaimportowane jako managed do TEST,
- connection references wskazują TEST,
- environment variables mają wartości TEST,
- flowy są poprawnie aktywowane,
- smoke test działa,
- E2E przechodzi,
- negative test tworzy ProcessLog,
- deployment record został wypełniony.

---

# Materiał Microsoft

- Import solutions: https://learn.microsoft.com/en-us/power-apps/maker/data-platform/import-update-export-solutions
- Power Platform pipelines: https://learn.microsoft.com/en-us/power-platform/alm/pipelines
- Connection references: https://learn.microsoft.com/en-us/power-apps/maker/data-platform/create-connection-reference
- Environment variables: https://learn.microsoft.com/en-us/power-apps/maker/data-platform/environmentvariables
