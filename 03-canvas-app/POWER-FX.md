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
