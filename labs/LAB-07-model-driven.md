# LAB 07 – Model-driven App: Contract Administration

## Cel laboratorium

Zbudować aplikację administracyjną Model-driven App na modelu Dataverse z LAB 05.

Celem nie jest poznanie każdej opcji Model-driven Apps, lecz zrozumienie kiedy aplikacja generowana z modelu danych jest lepszym wyborem niż rozbudowany Canvas App.

## Czas

60–75 minut.

## Wymagania

Ukończone LAB 05 i LAB 06.

---

# Zadanie 1 – Utworzenie aplikacji

1. Otwórz Solution `Vendor Contract Management DEV`.
2. **New -> App -> Model-driven app**.
3. Nazwa:

```text
VCM - Contract Administration
```

4. Create.

---

# Zadanie 2 – Navigation

W App Designer dodaj grupę:

```text
Contracts
```

Dodaj strony oparte na tabelach:

- Contracts,
- Suppliers,
- Approvals,
- Process Logs.

Ułóż kolejność:

```text
Contracts
Suppliers
Approvals
Process Logs
```

Zapisz.

---

# Zadanie 3 – Formularz Contract

Otwórz konfigurację table `Contract` -> Forms.

Edytuj Main Form.

Utwórz sekcje:

## General

- Contract Number,
- Supplier,
- Amount,
- Currency Code,
- Status.

## Dates

- Valid From,
- Valid To.

## Integration

- External System ID,
- Correlation ID.

## Ownership / requestor

- Requestor,
- Owner – jeśli przydatne.

Zapisz i opublikuj.

---

# Zadanie 4 – Related data

Dodaj na formularzu Contract subgrid `Approvals`:

- tabela powiązana: Approval,
- relacja: Contract -> Approval.

Dodaj drugi subgrid:

```text
Process Logs
```

Oczekiwany efekt:

```text
Contract form
|
+-- contract fields
|
+-- approvals history
|
+-- process/integration logs
```

To jest jedna z kluczowych przewag modelu relacyjnego dla aplikacji administracyjnej.

---

# Zadanie 5 – Widok Active Contracts

Dla table Contract utwórz view:

```text
VCM - Active Contracts
```

Kolumny:

- Contract Number,
- Supplier,
- Amount,
- Status,
- Valid To,
- External System ID.

Filtr:

```text
Status != Rejected
```

Sortowanie:

```text
Valid To ascending
```

---

# Zadanie 6 – Widok Integration Errors

Utwórz view:

```text
VCM - Integration Errors
```

Filtr:

```text
Status = Integration Error
```

Pokaż:

- Contract Number,
- Supplier,
- Correlation ID,
- External System ID,
- Modified On.

---

# Zadanie 7 – ProcessLog Errors

Dla Process Log utwórz view:

```text
VCM - Errors
```

Filtr:

```text
Severity = Error OR Severity = Critical
```

Sortuj malejąco po Timestamp.

---

# Zadanie 8 – Wyszukiwanie i nawigacja

Uruchom aplikację i wykonaj:

1. znajdź `VCM/2026/003`,
2. otwórz umowę,
3. przejdź do Supplier,
4. wróć do Contract,
5. przejrzyj Approvals,
6. przejrzyj Process Logs.

Zastanów się, ile ekranów i formuł trzeba byłoby zbudować ręcznie w Canvas App, aby osiągnąć podobny interfejs administracyjny.

---

# Zadanie 9 – Quick Create lub prosty formularz

Jeśli czas pozwala:

1. skonfiguruj szybkie tworzenie Approval,
2. pozostaw minimum pól:
   - Contract,
   - Approval Type,
   - Approver,
   - Status.

---

# Test końcowy

Scenariusz administratora:

1. Uruchom `VCM - Contract Administration`.
2. Otwórz Active Contracts.
3. Otwórz umowę.
4. Dodaj Approval.
5. Sprawdź Process Logs.
6. Zmień Status.
7. Sprawdź audit history, jeżeli dostępne.

---

# Pytania do dyskusji

1. Czy pracownik składający jedną umowę potrzebuje takiego interfejsu?
2. Czy administrator obsługujący 500 umów potrzebuje pięknego, całkowicie customowego Canvas UI?
3. Czy można użyć obu aplikacji na tym samym Dataverse?
4. Które reguły powinny być w aplikacji, które w flow, a które w warstwie danych?

---

# Kryterium ukończenia

- aplikacja zawiera cztery tabele,
- formularz Contract zawiera subgrid Approvals i Process Logs,
- istnieją widoki Active Contracts i Integration Errors,
- uczestnik potrafi wyjaśnić różnicę Canvas vs Model-driven w tym samym rozwiązaniu.

---

# Materiał Microsoft

- Model-driven apps overview: https://learn.microsoft.com/en-us/power-apps/maker/model-driven-apps/model-driven-app-overview
