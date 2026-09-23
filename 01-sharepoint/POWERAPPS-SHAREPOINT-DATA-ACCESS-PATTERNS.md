# Power Apps + SharePoint Online – wzorce dostępu do danych

## Cel

Dokument opisuje praktyczne wzorce odczytu i zapisu danych z Canvas App do SharePoint Online.

## 1. Odczyt danych

Preferuj delegowalne operacje wykonywane po stronie SharePoint:

```powerfx
Filter(
    Contracts,
    Status.Value = "Submitted"
)
```

Nie pobieraj całej listy do kolekcji tylko po to, aby filtrować ją lokalnie.

## 2. Filter vs LookUp

`Filter()` zwraca tabelę:

```powerfx
Filter(
    Contracts,
    Supplier.Id = varSupplierId
)
```

`LookUp()` zwraca pierwszy pasujący rekord:

```powerfx
LookUp(
    Contracts,
    ID = varContractId
)
```

Jeżeli identyfikator jest jednoznaczny, `LookUp()` lepiej komunikuje intencję.

## 3. Patch

`Patch()` jest dobry do częściowych aktualizacji i scenariuszy niestandardowych.

Przykład:

```powerfx
Patch(
    Contracts,
    LookUp(Contracts, ID = varContractId),
    {
        Status: { Value: "Submitted" }
    }
)
```

Nie aktualizuj pól, których nie trzeba zmieniać.

## 4. SubmitForm

`SubmitForm()` jest preferowany, gdy aplikacja używa kontrolki Edit Form i standardowych DataCard.

```powerfx
SubmitForm(frmContract)
```

Zalety:

- automatyczna integracja z Required,
- obsługa DataCard,
- prostszy lifecycle formularza,
- właściwości `OnSuccess`, `OnFailure`, `Valid`.

## 5. Patch vs SubmitForm

Użyj `SubmitForm`, gdy formularz jest głównym mechanizmem edycji rekordu.

Użyj `Patch`, gdy:

- aktualizujesz kilka wybranych pól,
- zapisujesz bez formularza,
- tworzysz niestandardową logikę zapisu,
- zapis obejmuje kilka źródeł danych.

## 6. ClearCollect i kolekcje

Kolekcja nie jest automatycznie cachem ani zamiennikiem delegacji.

```powerfx
ClearCollect(
    colContracts,
    Filter(Contracts, Status.Value = "Submitted")
)
```

Kolekcje mają sens dla:

- małych słowników,
- danych tymczasowych,
- lokalnego draftu,
- wyniku zwróconego przez flow lub API,
- danych potrzebnych do wielokrotnego przetwarzania po stronie klienta.

Nie używaj kolekcji do kopiowania dużej listy SharePoint.

## 7. With

`With()` upraszcza formuły i ogranicza wielokrotne wykonywanie tych samych wyrażeń.

```powerfx
With(
    {
        contractId: ThisItem.ID,
        newStatus: "Submitted"
    },
    Patch(
        Contracts,
        LookUp(Contracts, ID = contractId),
        {
            Status: { Value: newStatus }
        }
    )
)
```

## 8. Concurrent

`Concurrent()` może wykonywać niezależne operacje równolegle:

```powerfx
Concurrent(
    ClearCollect(colSuppliers, Suppliers),
    ClearCollect(colCurrencies, CurrencyDictionary)
)
```

Nie używaj `Concurrent()` dla operacji zależnych od siebie.

## 9. Refresh

`Refresh()` wykonuje ponowne pobranie danych ze źródła.

```powerfx
Refresh(Contracts)
```

Nie używaj go po każdej operacji. Nadmierne `Refresh()` zwiększa liczbę wywołań i pogarsza responsywność.

## 10. Optimistic vs confirmed update

Optimistic update:

```text
UI zmienia stan
-> zapis backend
-> ewentualny rollback UI
```

Confirmed update:

```text
zapis backend
-> potwierdzenie
-> UI zmienia stan
```

Dla operacji krytycznych preferuj confirmed update albo jawny mechanizm obsługi błędu.

## 11. Unikaj N+1

Anti-pattern:

```powerfx
AddColumns(
    Contracts,
    SupplierName,
    LookUp(Suppliers, ID = Supplier.Id).Title
)
```

wykonywany dla dużej liczby rekordów może generować wiele dodatkowych zapytań.

Rozważ:

- ograniczenie zbioru,
- denormalizację pola wyświetlanego,
- lokalny mały słownik,
- zmianę modelu danych.

## 12. Minimalny wzorzec zapisu

```powerfx
IfError(
    Patch(
        Contracts,
        LookUp(Contracts, ID = varContractId),
        {
            Status: { Value: "Submitted" }
        }
    ),
    Notify(
        "Nie udało się zapisać zmian.",
        NotificationType.Error
    ),
    Notify(
        "Zmiany zapisane.",
        NotificationType.Success
    )
)
```

## 13. Zasady

- deleguj filtrowanie do SharePoint,
- pobieraj tylko potrzebne dane,
- unikaj pełnych kopii list w kolekcjach,
- rozdziel odczyt, walidację i zapis,
- obsługuj błędy zapisu,
- nie zakładaj, że UI i SharePoint są zawsze w tym samym stanie.
