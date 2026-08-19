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
