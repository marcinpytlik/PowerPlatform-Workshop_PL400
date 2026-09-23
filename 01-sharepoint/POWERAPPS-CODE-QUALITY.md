# Power Apps – jakość kodu Power Fx

## Cel

Dokument opisuje zasady utrzymywalnego Power Fx.

## 1. Małe formuły

Jeżeli `OnSelect` ma setki linii, trudno go testować i reviewować.

Rozdziel:

```text
validation
-> save
-> notification
-> navigation
```

## 2. With zamiast powtórzeń

```powerfx
With(
    {
        amount: Value(txtAmount.Value),
        status: drpStatus.Selected.Value
    },
    ...
)
```

unika wielokrotnego odczytu tych samych wartości.

## 3. IfError

Obsługuj błędy operacji danych:

```powerfx
IfError(
    Patch(...),
    Notify(
        "Błąd zapisu",
        NotificationType.Error
    )
)
```

## 4. Errors

Po operacjach na źródle można analizować `Errors()`, gdy potrzebna jest bardziej szczegółowa diagnostyka.

## 5. Unikaj magic values

Zamiast powtarzać:

```powerfx
"Submitted"
```

w wielu miejscach, rozważ centralną reprezentację statusów lub konfigurację.

## 6. Komentarze

Komentarz powinien wyjaśniać decyzję, nie przepisywać kod.

Dobry:

```text
// Partial update, aby nie nadpisywać wartości edytowanych równolegle.
```

Słaby:

```text
// Ustaw status na Submitted.
```

## 7. Formatowanie

Stosuj jeden styl:

```powerfx
If(
    condition,
    actionTrue,
    actionFalse
)
```

zamiast wieloliniowych formuł bez czytelnych wcięć.

## 8. Side effects

Formuły wykonujące zapis, flow i nawigację powinny mieć jasną kolejność.

Nie ukrywaj wielu efektów ubocznych w wyrażeniach, których nazwa sugeruje tylko obliczenie.

## 9. Jedna odpowiedzialność

Button Submit powinien uruchamiać proces submit.

Jeżeli jednocześnie:

- czyści cache,
- zmienia użytkownika,
- importuje konfigurację,
- zapisuje trzy listy,

to odpowiedzialności są pomieszane.

## 10. Guard clauses

Najpierw waliduj warunki wejściowe:

```powerfx
If(
    !frmContract.Valid,
    Notify(...),
    SubmitForm(frmContract)
)
```

## 11. App Checker i Monitor

Quality nie kończy się na czytelności kodu.

Sprawdzaj również:

- delegation warnings,
- accessibility,
- connector errors,
- performance.

## 12. Review checklist

```text
[ ] czy formuła jest delegowalna?
[ ] czy zapis obsługuje błąd?
[ ] czy nie ma zbędnego Refresh?
[ ] czy nie ma N+1?
[ ] czy nazwy są czytelne?
[ ] czy logika biznesowa nie jest skopiowana?
[ ] czy security jest po stronie backendu?
```
