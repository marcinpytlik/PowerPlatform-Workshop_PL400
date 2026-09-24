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

## Checkpoint przed LAB

Przed większymi zmianami w modelu warto utworzyć ręczny backup środowiska, jeżeli typ środowiska i uprawnienia na to pozwalają:

```text
Power Platform admin center
-> Environments
-> <środowisko>
-> Backup & Restore
-> utwórz manual backup
```

Przykładowa nazwa:

```text
Before LAB05 Dataverse model
```

Backup środowiska jest mechanizmem platformy – nie jest to plik `.bak` do pobrania. Przywrócenie całego środowiska jest operacją znacznie szerszą niż odtworzenie pojedynczej tabeli, dlatego traktuj je jako checkpoint awaryjny.

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

> Logical/schema name tabeli i kolumn zależy od prefixu Publishera użytego przy tworzeniu komponentu. Jeżeli środowisko ma np. prefix `vcmmt`, tabela może mieć logical name `vcmmt_contract`. Display name `Contract` i logical name to dwie różne rzeczy.

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

Nie istnieje przełącznik Dataverse:

```text
Append-oriented = On
```

To decyzja projektowa. Każde istotne zdarzenie procesu powinno wykonywać:

```text
Dataverse -> Add a new row
```

zamiast aktualizować poprzedni wpis przez `Update a row`.

Przykładowy timeline:

```text
10:15  API Call   Error        HTTP 500
10:16  Retry      Information  Retry started
10:16  API Call   Information  HTTP 201
```

Każda linia to osobny rekord `Process Log`. Dzięki temu nie tracimy historii wcześniejszych prób i możemy odtworzyć przebieg po `Correlation ID`.

Jeżeli architektura wymaga mocniejszego wymuszenia tej zasady, rola używana przez proces może mieć dla `Process Log`:

```text
Create = Yes
Read   = Yes
Write  = No
Delete = No
```

Nie jest to wymagane do ukończenia LAB, ale dobrze pokazuje różnicę pomiędzy konwencją aplikacyjną a wymuszeniem security.

---

# Zadanie 8 – Auditing

Auditing musi być świadomie skonfigurowany na odpowiednich poziomach.

## 8.1 Auditing środowiska

W Power Platform admin center sprawdź ustawienia audytu środowiska:

```text
Environment
-> Settings
-> Audit and logs / Audit settings
```

Nazwy sekcji mogą się nieznacznie różnić w bieżącym interfejsie.

## 8.2 Auditing tabeli i kolumn

Włącz auditing dla tabeli `Contract`.

Minimum dla kolumn:

- Status,
- Amount,
- Supplier,
- Valid To,
- External System ID.

Audyt zaczyna rejestrować zmiany od momentu jego włączenia. Nie oczekuj historii zmian wykonanych wcześniej.

## 8.3 Test

1. Utwórz lub otwórz testową umowę.
2. Ustaw np. `Status = Submitted`.
3. Zapisz.
4. Zmień status na `In Approval`.
5. Zapisz ponownie.

## 8.4 Gdzie sprawdzić Audit History

Najczytelniej robi się to z formularza konkretnego rekordu w Model-driven app:

```text
Model-driven app
-> Contracts
-> otwórz konkretny rekord
-> Related / Powiązane
-> Audit History
```

W zależności od wersji UI opcja może być też schowana pod menu `...`.

> Widok `Tables -> Contract -> Data` w make.powerapps.com jest edytorem danych tabeli i nie pokazuje tego samego menu `Related` co formularz rekordu w Model-driven app.

W historii znajdź zmianę starej i nowej wartości, np.:

```text
Status: Submitted -> In Approval
```

---

# Zadanie 9 – Security role

Utwórz **Dataverse Security Role**:

```text
VCM Contract User
```

Nie myl jej z rolą środowiskową `Environment Maker`. Rola maker pozwala tworzyć komponenty w środowisku, ale nie zastępuje uprawnień do danych wynikających z Dataverse security roles.

## 9.1 Wariant szkoleniowy dla User or team owned

Dla rekomendowanego ownership `User or team owned` ustaw przykładowo:

| Table | Privilege | Access level |
|---|---|---|
| Supplier | Read | Organization |
| Supplier | Append To | Organization |
| Contract | Create | User |
| Contract | Read | User |
| Contract | Write | User |
| Contract | Append | User |
| Contract | Append To | User |
| Approval | Read | Organization |
| Process Log | Read | Organization |

Na tym etapie nie dawaj automatycznie `Delete`, `Assign` i `Share`, jeśli proces ich nie wymaga.

## 9.2 Dlaczego Append / Append To

Samo `Read` nie zawsze wystarczy do pracy z lookupami.

Dla relacji:

```text
Contract -> Supplier
```

użytkownik musi mieć odpowiednie uprawnienia pozwalające powiązać rekordy. W uproszczeniu szkoleniowym:

```text
Contract -> Append
Supplier -> Append To
```

Analogicznie trzeba przeanalizować lookupi:

```text
Approval -> Contract
Process Log -> Contract
```

gdy użytkownik lub flow ma tworzyć takie rekordy.

## 9.3 Trzy osobne pojęcia

```text
Security Role
= jakie operacje użytkownik może wykonać

Ownership
= kto jest właścicielem rekordu

Access level
= jak szeroki jest zakres rekordu dla danego privilege
```

Dla tabel User or team owned poziom `User` dobrze pokazuje row-level security: użytkownik może mieć `Read` do Contract, ale tylko dla rekordów w swoim zakresie.

## 9.4 Administrator

Utwórz drugą rolę koncepcyjnie:

```text
VCM Contract Administrator
```

z szerszymi uprawnieniami, np. organizacyjnym Create/Read/Write dla tabel biznesowych. `Delete`, `Assign` i `Share` dodawaj tylko, jeżeli wymagają tego zadania administratora.

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

## Gdy lookup Supplier nic nie pokazuje

Jeżeli ręcznie utworzyłeś rekord `Supplier`, ale lookup w `Contract` jest pusty:

1. potwierdź, że pracujesz w tym samym Environment,
2. otwórz `Tables -> Supplier -> Data` i sprawdź, czy rekord istnieje,
3. w `Contract` sprawdź definicję kolumny `Supplier`:
   - Type = Lookup,
   - Related table = Supplier,
4. użyj przycisku `Refresh` w pasku nad widokiem danych tabeli,
5. ponownie otwórz lookup.

W widoku danych przycisk znajduje się typowo obok:

```text
New row | New column | Refresh | ...
```

Samo utworzenie definicji tabeli `Contract` nie kopiuje danych z SharePoint do Dataverse. Migracja danych jest osobnym krokiem w LAB 06.

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

# Awaryjne odtworzenie modelu

Usunięcie całej custom table to nie to samo co usunięcie pojedynczego row. Deleted records / recycle mechanizmy dla rekordów nie są mechanizmem przywracania definicji tabeli.

Jeżeli tabela została przypadkowo usunięta:

1. dla świeżego LAB zwykle najszybciej odtworzyć ją z definicji w tym dokumencie,
2. jeżeli środowisko zawiera ważne dane i zależności, rozważ restore całego środowiska z backupu,
3. sprawdź relacje w tabelach zależnych, ponieważ lookupi do usuniętej tabeli mogły również zniknąć,
4. po ręcznym odtworzeniu sprawdź flowy i aplikacje, które odwoływały się do poprzedniego komponentu.

Przykład dla usuniętego `Contract`:

```text
Contract
+ Supplier lookup
+ alternate key
+ auditing
+ Approval -> Contract
+ Process Log -> Contract
```

Model można również provisionować skryptem przez Dataverse Web API / narzędzia ALM. Na szkoleniu robimy model ręcznie, aby uczestnik poznał interfejs i zależności; automatyzacja provisioningu jest dobrym rozszerzeniem dla repozytorium developerskiego.

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
- Security roles and privileges: https://learn.microsoft.com/en-us/power-platform/admin/security-roles-privileges
- Backup and restore environments: https://learn.microsoft.com/en-us/power-platform/admin/backup-restore-environments
- Dataverse Web API metadata: https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/create-update-entity-definitions-using-web-api
