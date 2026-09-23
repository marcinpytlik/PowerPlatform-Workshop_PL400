# Power Apps – stan, zmienne i kolekcje

## Cel

Dokument opisuje zarządzanie stanem w Canvas App.

## 1. Rodzaje stanu

Najczęściej występują:

- stan globalny aplikacji,
- stan ekranu,
- stan kontrolki,
- stan rekordu backendowego,
- dane tymczasowe,
- cache lokalny.

Nie należy mieszać tych pojęć.

## 2. Set

`Set()` tworzy zmienną globalną:

```powerfx
Set(
    varCurrentContractId,
    ThisItem.ID
)
```

Używaj dla wartości potrzebnych na wielu ekranach.

## 3. UpdateContext

`UpdateContext()` tworzy stan kontekstowy ekranu:

```powerfx
UpdateContext(
    {
        locEditMode: true
    }
)
```

Preferuj go dla stanu lokalnego ekranu.

## 4. With

Jeżeli wartość jest potrzebna tylko wewnątrz jednej formuły, preferuj `With()` zamiast tworzenia globalnej zmiennej.

```powerfx
With(
    {
        amount: Value(txtAmount.Value)
    },
    If(
        amount > 100000,
        "Finance approval",
        "Legal approval"
    )
)
```

## 5. Collections

Kolekcje są tabelami w pamięci aplikacji.

```powerfx
ClearCollect(
    colDraftLines,
    ...
)
```

Używaj dla danych tymczasowych, ale nie jako domyślnego zamiennika backendu.

## 6. Named formulas

Jeżeli środowisko i wersja aplikacji wspierają named formulas, mogą zastąpić część inicjalizacji w `App.OnStart`.

Dobre zastosowania:

- stałe,
- wartości pochodne,
- konfiguracja,
- logika bez efektów ubocznych.

## 7. App.OnStart

Nie umieszczaj całej logiki aplikacji w `App.OnStart`.

Problemy:

- wolniejszy start,
- trudniejsza diagnostyka,
- zależność ekranów od kolejności inicjalizacji,
- trudniejsze testowanie.

## 8. Ekran jako granica stanu

Dobrą praktyką jest ograniczenie liczby zmiennych globalnych.

Przykład:

```text
Screen ContractEdit
    locContract
    locIsSaving
    locValidationMessage
```

zamiast:

```text
var1
var2
var3
var4
...
```

## 9. Backend jest źródłem prawdy

Zmienne Power Apps nie powinny być jedynym miejscem przechowywania stanu biznesowego.

```text
varStatus = "Approved"
```

nie oznacza, że kontrakt jest zatwierdzony.

Stan biznesowy powinien zostać zapisany w SharePoint/Dataverse/API.

## 10. Reset

Po zakończeniu operacji resetuj stan, który nie powinien przechodzić do kolejnego procesu:

```powerfx
ResetForm(frmContract);
UpdateContext({ locEditMode: false })
```

## 11. Anti-patterny

- dziesiątki globalnych `Set()`,
- kolekcja jako kopia całej listy SharePoint,
- logika biznesowa oparta tylko na stanie klienta,
- `App.OnStart` zawierający cały proces aplikacji,
- zmienne o nazwach `var1`, `tmp`, `flag`.

## 12. Zasada

Używaj najmniejszego możliwego zakresu stanu:

```text
With
-> context variable
-> global variable
-> collection
```

dopiero gdy rzeczywiście potrzebujesz większego zakresu.
