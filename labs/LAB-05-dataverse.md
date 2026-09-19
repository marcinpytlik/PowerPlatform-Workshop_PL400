# LAB 05 – Dataverse: docelowy model danych

## Cel laboratorium

Zbudować docelowy model relacyjny aplikacji Vendor Contract Management w Dataverse i porównać go z modelem SharePoint.

Po laboratorium uczestnik potrafi:

- utworzyć custom tables,
- dobrać typy kolumn,
- tworzyć relacje 1:N,
- tworzyć Choice,
- definiować alternate keys,
- włączyć auditing,
- utworzyć podstawową security role,
- wyjaśnić różnicę między właścicielem rekordu, security role i uprawnieniem do tabeli.

## Czas

100–120 minut. W agendzie 3-dniowej: **105 min**. Relacje N:N są tematem dyskusji, nie częścią modelu VCM.

## Wymagania

Środowisko z Dataverse oraz uprawnienia maker.

---

# Model końcowy

```text
Supplier
  1
  |
  N
Contract
  1
  +---------- N Approval
  |
  +---------- N Process Log
```

---

# Zadanie 1 – Utworzenie docelowego Publishera i Solution

Pełny ALM omawiamy później, ale już teraz tworzymy **docelowego Publishera i jedno docelowe Solution**. Nie używaj tymczasowego publishera, ponieważ prefix schematu komponentów zostaje nadany przy ich tworzeniu.

1. Otwórz `make.powerapps.com`.
2. Wybierz **Solutions**.
3. **New solution**.
4. Utwórz Publisher:
   - Display name: `Vendor Contract Management`
   - Name: `VendorContractManagement`
   - Prefix: `vcm`
5. Utwórz Solution:
   - Display name: `Vendor Contract Management`
   - Name: `VendorContractManagement`
   - Publisher: `Vendor Contract Management`
   - Version: `0.5.0.0`
6. Create.

> To samo Solution będzie rozwijane do końca szkolenia. W LAB Solutions/ALM podniesiemy wersję do `1.0.0.0`, zamiast tworzyć drugie rozwiązanie.

---

# Zadanie 2 – Choice definitions

Utwórz choices wymagane przez model.

## Contract Status

```text
Draft
Submitted
In Approval
Approved
Rejected
Integration Pending
Integrated
Integration Error
```

## Approval Type

```text
Legal
Finance
Management
```

## Approval Status

```text
Pending
Approved
Rejected
Cancelled
```

## Log Severity

```text
Information
Warning
Error
Critical
```

Nazwy schema powinny używać prefixu `vcm`.

---

# Zadanie 3 – Supplier

W Solution:

1. **New -> Table -> Table**.
2. Display name: `Supplier`.
3. Plural name: `Suppliers`.
4. Primary column: `Name`.
5. Ownership: dobierz zgodnie z potrzebami laboratorium – rekomendowany wariant to User or team owned, aby móc później omówić row-level security.
6. Create.

Dodaj kolumny:

| Display Name | Type | Required |
|---|---|---:|
| Supplier Code | Text | Business required |
| Tax ID | Text | Optional |
| Country | Text | Required |
| Active | Yes/No | Required |

Default Active = Yes.

## Alternate key

1. Otwórz właściwości tabeli Supplier.
2. Przejdź do Keys.
3. New key.
4. Name: `AK_Supplier_SupplierCode`.
5. Columns: `Supplier Code`.
6. Save.

Po utworzeniu status klucza może być początkowo Pending. Poczekaj, aż zostanie aktywowany.

---

# Zadanie 4 – Contract

Utwórz tabelę `Contract`.

Primary column:

```text
Contract Number
```

Dodaj:

| Display Name | Type |
|---|---|
| Amount | Currency |
| Currency Code | Choice: PLN, EUR, USD – ten sam zestaw co SharePoint |
| Valid From | Date only |
| Valid To | Date only |
| Status | Choice: Contract Status |
| Requestor | Lookup -> User |
| External System ID | Text |
| Correlation ID | Text |

Default Status = Draft.

## Alternate key

Utwórz:

```text
AK_Contract_ContractNumber
```

na `Contract Number`.

---

# Zadanie 5 – Relacja Supplier -> Contract

1. Otwórz table `Contract`.
2. Dodaj Lookup column `Supplier`.
3. Related table: `Supplier`.
4. Required: Business required.
5. Save.

Lookup tworzy relację N:1 od Contract do Supplier, czyli z perspektywy Supplier mamy 1:N Contracts.

Sprawdź zakładkę Relationships.

---

# Zadanie 6 – Approval

Utwórz tabelę `Approval`.

Primary name może być tekstem automatycznie wypełnianym przez flow, np.:

```text
<ContractNumber> - Finance
```

Dodaj:

- Contract – Lookup -> Contract,
- Approval Type – Choice,
- Approver – Lookup -> User,
- Status – Choice,
- Decision Date – Date and time,
- Comment – Multiline text.

Relacja:

```text
Contract 1 -> N Approval
```

---

# Zadanie 7 – Process Log

Utwórz tabelę `Process Log`.

Dodaj:

| Kolumna | Typ |
|---|---|
| Contract | Lookup -> Contract |
| Flow Name | Text |
| Flow Run ID | Text |
| Correlation ID | Text |
| Timestamp | Date and time |
| Action Name | Text |
| Severity | Choice: Log Severity |
| HTTP Status | Whole Number |
| Error Code | Text |
| Message | Multiline text |

Ustal, że log jest **append-oriented**: proces tworzy kolejne rekordy zamiast nadpisywać jeden „ostatni błąd”.

---

# Zadanie 8 – Auditing

Włącz auditing zgodnie z aktualnym interfejsem środowiska.

Minimum:

- table Contract,
- kolumny Status,
- Amount,
- Supplier,
- Valid To,
- External System ID.

> Auditing może wymagać włączenia na poziomie środowiska. 

Po włączeniu:

1. zmień Status testowej umowy,
2. zapisz,
3. otwórz audit history rekordu, jeśli UI i uprawnienia to umożliwiają,
4. znajdź zmianę starej i nowej wartości.

---

# Zadanie 9 – Security role

Utwórz rolę:

```text
VCM Contract User
```

Minimalny cel szkoleniowy:

- Supplier: Read,
- Contract: Create, Read, Write,
- Approval: Read,
- Process Log: Read – opcjonalnie ogranicz do wsparcia technicznego.

Zakres uprawnień dopasuj do modelu ownership.

Następnie utwórz drugą rolę koncepcyjnie:

```text
VCM Contract Administrator
```

z szerszymi uprawnieniami.

Omów zasadę least privilege.

---

# Zadanie 10 – Dane testowe

Dodaj dostawców oraz umowy analogiczne do LAB 01.

Dla `VCM/2026/003` ustaw:

```text
Amount = 650000
Status = Submitted
```

Dodaj jeden Approval oraz jeden ProcessLog.

---

# Zadanie 11 – Porównanie modelu

Uzupełnij tabelę podczas zajęć:

| Cecha | SharePoint | Dataverse |
|---|---|---|
| Business key | | |
| Relacje | | |
| Row-level security | | |
| Audit | | |
| Model-driven app | | |
| Delegacja / query | | |
| Koszt/licencja | | |
| Prostota wdrożenia | | |

---

# Test końcowy

1. Spróbuj utworzyć dwóch Supplier z tym samym `Supplier Code` po aktywacji alternate key.
2. Sprawdź, czy drugi zapis jest blokowany.
3. Otwórz Supplier i przejdź do powiązanych Contracts.
4. Zmień Status umowy.
5. Sprawdź audit history.
6. Utwórz ProcessLog powiązany z Contract.

---

# Kryterium ukończenia

- 4 tabele istnieją w Solution,
- relacje 1:N działają,
- Choices są współdzielone lub konsekwentnie skonfigurowane,
- alternate keys są aktywne,
- auditing jest włączony przynajmniej dla Contract,
- istnieje rola `VCM Contract User`.

## Po tym LAB

Talk track: **Source of Truth**, State Machine. Pełna ścieżka statusów VCM, łącznie z Integration Pending / Integration Error.

---

# Materiał Microsoft

- Create and edit Dataverse tables: https://learn.microsoft.com/en-us/power-apps/maker/data-platform/create-edit-entities-portal
- Column data types: https://learn.microsoft.com/en-us/power-apps/maker/data-platform/types-of-fields
- Build your data model with Dataverse: https://learn.microsoft.com/en-us/training/paths/build-data-model-microsoft-dataverse/
- Manage Dataverse auditing: https://learn.microsoft.com/en-us/power-platform/admin/manage-dataverse-auditing
