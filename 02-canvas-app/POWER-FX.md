# Power Fx – przykładowe fragmenty

## Walidacja formularza

```powerfx
If(
    IsBlank(txtContractNumber.Text) || IsBlank(cmbSupplier.Selected),
    Notify("Uzupełnij wymagane pola", NotificationType.Error),
    SubmitForm(frmContract)
)
```

## Filtrowanie

```powerfx
Filter(
    Contracts,
    Status.Value = "Submitted"
)
```

Po LAB 06 źródłem jest Dataverse: numer umowy to primary name (`Contract Number`), nie SharePoint `Title`. `Status.Value` zostaje.

## Bezpieczniejsza konfiguracja języka

```powerfx
Set(varLanguage, Left(Language(), 2))
```

## Trace

```powerfx
Trace(
    "Contract form submitted",
    TraceSeverity.Information,
    { ContractNumber: txtContractNumber.Text }
)
```


---

## Dalej: wzorce projektowe

Przejdź do [DESIGN-PATTERNS.md](DESIGN-PATTERNS.md), gdzie opisane są m.in. Separation of Concerns, State Management, Delegation First, Navigation Parameters, Lazy Loading i anti-patterns Canvas Apps.
