# Power Apps – konwencje nazewnicze

## Cel

Spójne nazwy skracają czas debugowania i review.

## 1. Kontrolki

Przykładowe prefiksy:

| Typ | Prefix | Przykład |
|---|---|---|
| Gallery | `gal` | `galContracts` |
| Form | `frm` | `frmContract` |
| Button | `btn` | `btnSubmit` |
| Label | `lbl` | `lblStatus` |
| Text input | `txt` | `txtSearch` |
| Dropdown | `drp` | `drpStatus` |
| Combo box | `cmb` | `cmbSupplier` |
| Toggle | `tog` | `togActive` |
| Container | `con` | `conHeader` |
| Icon | `ico` | `icoRefresh` |

## 2. Zmienne

Global:

```text
varCurrentUser
varCurrentContractId
```

Context:

```text
locEditMode
locIsSaving
```

Collections:

```text
colContracts
colSuppliers
```

## 3. Flow

Nazwy powinny opisywać działanie:

```text
VCM - Contract Submitted
VCM - Approval
VCM - API Integration
```

Nie używaj:

```text
Flow1
NewFlow
Test2
```

## 4. SharePoint lists

Używaj stabilnych nazw technicznych.

Zmiana display name nie powinna ukrywać znaczenia internal names.

## 5. Kolumny

Preferuj jednoznaczne nazwy:

```text
SupplierCode
RequestorEmail
ExternalSystemId
CorrelationId
```

zamiast:

```text
Code
Email
Id2
Field1
```

## 6. Ekrany

```text
scrHome
scrContractList
scrContractEdit
scrSettings
```

## 7. Komponenty

```text
cmpHeader
cmpStatusBadge
cmpConfirmDialog
```

## 8. Zasada

Nazwa powinna odpowiadać na pytanie:

```text
co to jest?
do czego służy?
jaki ma zakres?
```
