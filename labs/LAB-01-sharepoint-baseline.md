# LAB 01 – SharePoint baseline: model danych Vendor Contract Management

## Cel laboratorium

Zbudować od zera początkowy model danych oparty na SharePoint/Microsoft Lists, który będzie używany przez Canvas App oraz pierwsze flowy Power Automate. Ten model jest celowo prosty – w dalszej części szkolenia zostanie porównany i częściowo zastąpiony modelem Dataverse.

Po zakończeniu laboratorium uczestnik potrafi:

- utworzyć listy biznesowe w SharePoint,
- dobrać podstawowe typy kolumn,
- zdefiniować kolumnę Lookup,
- utworzyć indeksy dla kolumn używanych w filtrach,
- przygotować widoki robocze,
- wprowadzić dane testowe,
- wskazać pierwsze ograniczenia SharePoint jako źródła danych aplikacji.

## Czas

60–75 minut.

## Wymagania

- dostęp do witryny SharePoint Online,
- uprawnienie do tworzenia list i kolumn,
- jedna witryna szkoleniowa, np. `PowerPlatformWorkshop`,
- konto używane później w Power Apps i Power Automate.

> Nazwy opcji w interfejsie mogą być wyświetlane po polsku lub angielsku. W instrukcji podawane są obie nazwy tam, gdzie ma to znaczenie.

---

## Architektura po LAB 01

```text
SharePoint Site
|
+-- Suppliers
|
+-- Contracts
|
+-- ContractApprovals
```

Relacje logiczne:

```text
Suppliers 1 ---- N Contracts
Contracts 1 ---- N ContractApprovals
```

---

# Zadanie 1 – Utworzenie listy Suppliers

1. Otwórz witrynę SharePoint używaną podczas szkolenia.
2. Wybierz **New / Nowy**.
3. Wybierz **List / Lista**.
4. Wybierz **Blank list / Pusta lista**.
5. Nazwa listy: `Suppliers`.
6. Opcjonalny opis: `Vendor Contract Management - supplier master data`.
7. Wybierz **Create / Utwórz**.

Domyślna kolumna `Title` zostanie wykorzystana jako nazwa dostawcy. Nie usuwaj jej.

## Dodaj kolumny

### SupplierCode

1. Wybierz **Add column / Dodaj kolumnę**.
2. Typ: **Single line of text / Jeden wiersz tekstu**.
3. Name: `SupplierCode`.
4. Required: **Yes**.
5. Zapisz.

### TaxId

- typ: Single line of text,
- nazwa: `TaxId`,
- required: No.

### Country

- typ: Single line of text,
- nazwa: `Country`,
- required: Yes.

### Active

- typ: Yes/No,
- nazwa: `Active`,
- wartość domyślna: Yes.

## Zmień nazwę kolumny Title na ekranie użytkownika

Jeżeli chcesz zachować czytelniejszy interfejs:

1. Otwórz menu kolumny `Title`.
2. **Column settings -> Edit**.
3. Display name: `SupplierName`.
4. Zapisz.

> Wewnętrzna nazwa SharePoint nadal może pozostać `Title`. Jest to celowo omawiane później jako różnica między nazwą wyświetlaną i nazwą techniczną.

---

# Zadanie 2 – Utworzenie listy Contracts

1. Utwórz nową pustą listę.
2. Nazwa: `Contracts`.
3. Kolumna `Title` będzie przechowywać numer umowy.
4. Zmień jej nazwę wyświetlaną na `ContractNumber`.

Dodaj kolumny:

| Kolumna | Typ | Wymagana | Uwagi |
|---|---|---:|---|
| Supplier | Lookup | Tak | źródło: Suppliers, kolumna SupplierName/Title |
| Amount | Currency | Tak | 2 miejsca dziesiętne |
| Currency | Choice | Tak | PLN, EUR, USD |
| ValidFrom | Date | Tak | tylko data |
| ValidTo | Date | Tak | tylko data |
| Status | Choice | Tak | Draft, Submitted, In Approval, Approved, Rejected, Integration Pending, Integrated, Integration Error |
| RequestorEmail | Single line of text | Tak | adres zgłaszającego |
| ExternalSystemId | Single line of text | Nie | ID zwrócone przez API |
| CorrelationId | Single line of text | Nie | identyfikator procesu |

## Lookup Supplier

1. **Add column -> Lookup**.
2. Name: `Supplier`.
3. Source list: `Suppliers`.
4. Source column: `SupplierName` lub `Title`.
5. Nie dodawaj na tym etapie dodatkowych pól z tabeli dostawców.
6. Zapisz.

## Status

Utwórz Choice z wartościami dokładnie w tej kolejności:

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

Default value: `Draft`.

## Currency

Wartości:

```text
PLN
EUR
USD
```

Default: `PLN`.

---

# Zadanie 3 – Utworzenie ContractApprovals

1. Utwórz pustą listę `ContractApprovals`.
2. Kolumnę Title możesz pozostawić, ale ustaw ją jako niewymaganą, jeżeli tenant na to pozwala.
3. Dodaj:

| Kolumna | Typ | Wartości / źródło |
|---|---|---|
| Contract | Lookup | Contracts -> ContractNumber/Title |
| ApprovalType | Choice | Legal, Finance, Management |
| ApproverEmail | Single line of text | adres osoby zatwierdzającej |
| Status | Choice | Pending, Approved, Rejected |
| DecisionDate | Date and time | data i czas |
| Comment | Multiple lines of text | plain text |

Status domyślny: `Pending`.

---

# Zadanie 4 – Indeksy

Indeksy są potrzebne, ponieważ w kolejnych laboratoriach będziemy filtrować duże listy.

Dla `Contracts`:

1. Otwórz **Settings / Ustawienia listy**.
2. Przejdź do **Indexed columns / Kolumny indeksowane**.
3. Utwórz indeks dla `Status`.
4. Utwórz indeks dla `Supplier`.
5. Jeżeli `ValidTo` będzie używane do raportowania kończących się umów, dodaj również indeks dla `ValidTo`.

Dla `ContractApprovals` dodaj indeks dla `Contract` oraz `Status`.

## Kontrola

Powinieneś mieć co najmniej:

```text
Contracts
- Status
- Supplier
- ValidTo

ContractApprovals
- Contract
- Status
```

---

# Zadanie 5 – Widoki

## Contracts – Active Contracts

1. Otwórz listę `Contracts`.
2. Utwórz nowy widok.
3. Nazwa: `Active Contracts`.
4. Pokaż kolumny:
   - ContractNumber,
   - Supplier,
   - Amount,
   - Currency,
   - ValidFrom,
   - ValidTo,
   - Status.
5. Filtr:

```text
Status is not equal to Rejected
```

6. Sortowanie: `ValidTo` rosnąco.

## Contracts – Expiring Contracts

Utwórz drugi widok `Expiring Contracts`. Na tym etapie nie musimy tworzyć dynamicznego filtra „30 dni”; wystarczy widok posortowany rosnąco po `ValidTo`. Dynamiczne oznaczanie zrobimy w Canvas App.

---

# Zadanie 6 – Dane testowe

Dodaj co najmniej trzech dostawców:

| SupplierName | SupplierCode | TaxId | Country | Active |
|---|---|---|---|---|
| Contoso Polska | SUP-001 | 1111111111 | PL | Yes |
| Fabrikam GmbH | SUP-002 | DE999999999 | DE | Yes |
| Northwind Services | SUP-003 | 2222222222 | PL | Yes |

Dodaj co najmniej pięć umów:

| ContractNumber | Supplier | Amount | Currency | Status |
|---|---|---:|---|---|
| VCM/2026/001 | Contoso Polska | 50000 | PLN | Draft |
| VCM/2026/002 | Fabrikam GmbH | 150000 | EUR | Submitted |
| VCM/2026/003 | Northwind Services | 650000 | PLN | Submitted |
| VCM/2026/004 | Contoso Polska | 25000 | PLN | Approved |
| VCM/2026/005 | Fabrikam GmbH | 90000 | EUR | Rejected |

Dla `VCM/2026/002` dodaj rekord `ContractApprovals`:

```text
ApprovalType: Finance
ApproverEmail: <adres szkoleniowy>
Status: Pending
```

---

# Test końcowy

Wykonaj ręcznie scenariusz:

1. Utwórz nowego dostawcę.
2. Utwórz dla niego nową umowę.
3. Wybierz dostawcę przez Lookup.
4. Ustaw Status=`Submitted`.
5. Utwórz rekord Approval związany z umową.
6. Otwórz `Active Contracts` i sprawdź, czy rekord jest widoczny.

## Kryterium ukończenia

LAB jest ukończony, gdy:

- istnieją trzy listy,
- lookupy działają,
- można ręcznie zapisać cały przypadek biznesowy,
- indeksy zostały utworzone,
- istnieje co najmniej pięć umów testowych.

## Po tym LAB

Nazwij ograniczenia SharePoint jako źródła prawdy. Wzorzec **Strangler Migration** zostaw na LAB 06 – dziś tylko ból, nie lek.

---

# Pytania do dyskusji

1. Co stanie się, gdy potrzebujemy kilku adresów dostawcy?
2. Jak wymusić unikalność `SupplierCode` oraz `ContractNumber`?
3. Czy Lookup w SharePoint daje nam takie same możliwości jak foreign key w relacyjnej bazie danych?
4. Co stanie się z procesem, jeżeli nazwa dostawcy zostanie zmieniona?
5. Gdzie będziemy trzymać pełny audyt zmian statusu?

---

# Najczęstsze problemy

## Nie widzę listy w Lookup

Sprawdź, czy listy znajdują się w tej samej witrynie SharePoint i czy konto ma do nich dostęp.

## Nie mogę utworzyć indeksu

Sprawdź typ kolumny oraz uprawnienia do zarządzania listą.

## Formularz pokazuje `Title`

To normalne. `Title` jest wewnętrzną kolumną SharePoint. Nazwa wyświetlana może zostać zmieniona na `ContractNumber` lub `SupplierName`.

---

# Materiał Microsoft

- SharePoint connector actions and triggers: https://learn.microsoft.com/en-us/sharepoint/dev/business-apps/power-automate/sharepoint-connector-actions-triggers
- SharePoint connector: https://learn.microsoft.com/en-us/connectors/sharepointonline/
