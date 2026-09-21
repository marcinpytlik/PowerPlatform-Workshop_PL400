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


## Notatki rozszerzające – Power Apps + SharePoint Online

- [SHAREPOINT-LIMITS-AND-CONSTRAINTS.md](SHAREPOINT-LIMITS-AND-CONSTRAINTS.md) – limity list i bibliotek, delegacja, lookupy, security scopes i ograniczenia backendu.
- [WHEN-TO-USE-SPFX-WEBPART.md](WHEN-TO-USE-SPFX-WEBPART.md) – kiedy użyć SPFx, Power Apps albo własnej aplikacji.
- [POWERAPPS-SHAREPOINT-DELEGATION.md](POWERAPPS-SHAREPOINT-DELEGATION.md) – delegacja, typy pól i typowe pułapki formuł Power Fx.
- [POWERAPPS-SHAREPOINT-PERFORMANCE.md](POWERAPPS-SHAREPOINT-PERFORMANCE.md) – N+1, App.OnStart, lazy loading, Refresh i Live Monitor.
- [SHAREPOINT-POWER-AUTOMATE-PATTERNS.md](SHAREPOINT-POWER-AUTOMATE-PATTERNS.md) – triggery, Get changes, Get items, concurrency, retry i correlation ID.
- [SHAREPOINT-SECURITY-AND-CONNECTIONS.md](SHAREPOINT-SECURITY-AND-CONNECTIONS.md) – sharing, permissions, connection owner, service accounts, DLP i Connection References.
- [POWERAPPS-SHAREPOINT-FORMS.md](POWERAPPS-SHAREPOINT-FORMS.md) – standardowy formularz, Customize Forms, Canvas App i SPFx Form Customizer.
- [SHAREPOINT-DOCUMENTS-AND-ATTACHMENTS.md](SHAREPOINT-DOCUMENTS-AND-ATTACHMENTS.md) – attachments, biblioteki dokumentów, metadata i versioning.
- [POWERAPPS-ERROR-HANDLING.md](POWERAPPS-ERROR-HANDLING.md) – IfError, Errors, Patch, walidacja i obsługa błędów.
- [POWERAPPS-SHAREPOINT-DIAGNOSTICS.md](POWERAPPS-SHAREPOINT-DIAGNOSTICS.md) – App Checker, Live Monitor, Run History, Version History i correlation ID.
