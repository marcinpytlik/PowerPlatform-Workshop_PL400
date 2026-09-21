# Model SharePoint – wersja początkowa

## Suppliers

- Title – nazwa dostawcy
- SupplierCode – tekst, unikalny biznesowo
- TaxId – tekst
- Country – tekst
- Active – Yes/No

## Contracts

- Title – numer umowy
- Supplier – Lookup do Suppliers
- Amount – Currency
- Currency – Choice
- ValidFrom – Date
- ValidTo – Date
- Status – Choice
- RequestorEmail – tekst
- ExternalSystemId – tekst
- CorrelationId – tekst

## ContractApprovals

- Contract – Lookup do Contracts
- ApprovalType – Choice: Legal / Finance / Management
- ApproverEmail – tekst
- Status – Choice
- DecisionDate – DateTime
- Comment – multiline text

## Zalecenia

- indeksować kolumny używane w filtrach,
- nie pobierać całych list bez Filter Query,
- nie traktować lookupów SharePoint jako pełnego modelu relacyjnego.


---

## Ograniczenia SharePoint jako backendu aplikacji

Przed LAB 05 warto przeczytać [SHAREPOINT-LIMITS-AND-CONSTRAINTS.md](SHAREPOINT-LIMITS-AND-CONSTRAINTS.md). Dokument zbiera limity list i bibliotek, delegację Power Apps, problemy z lookupami, security scopes, Get items, throttling, trigger loops oraz kryteria przejścia do Dataverse.


## Kiedy używać własnego webparta / SPFx

Zobacz [WHEN-TO-USE-SPFX-WEBPART.md](WHEN-TO-USE-SPFX-WEBPART.md). Materiał pokazuje, kiedy wybrać standardowy SharePoint, Power Apps, SPFx albo pełną aplikację customową oraz dlaczego SPFx nie usuwa ograniczeń SharePoint jako backendu.
