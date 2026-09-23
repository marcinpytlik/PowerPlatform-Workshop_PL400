# Power Apps + SharePoint Online – typy pól

## Cel

Dokument opisuje typowe reprezentacje kolumn SharePoint w Power Fx oraz sposób ich odczytu i zapisu.

## 1. Single line of text

Odczyt:

```powerfx
ThisItem.Title
```

lub przy spolszczonej nazwie wyświetlanej:

```powerfx
ThisItem.Tytuł
```

Zapis:

```powerfx
Patch(
    Contracts,
    ThisItem,
    { Title: txtTitle.Value }
)
```

## 2. Number / Currency

Odczyt:

```powerfx
ThisItem.Amount
```

Formatowanie:

```powerfx
Text(
    ThisItem.Amount,
    "[$-pl-PL]#,##0.00 zł"
)
```

Zapis:

```powerfx
{ Amount: Value(txtAmount.Value) }
```

## 3. Yes/No

Odczyt:

```powerfx
ThisItem.Active
```

Zapis:

```powerfx
{ Active: togActive.Checked }
```

## 4. Choice – pojedynczy wybór

Odczyt:

```powerfx
ThisItem.Status.Value
```

Zapis:

```powerfx
{
    Status: {
        Value: "Submitted"
    }
}
```

W formularzu ComboBox zwykle pracuje na rekordzie Choice, nie na zwykłym tekście.

## 5. Choice – wiele wartości

Wartość jest tabelą rekordów.

Przykładowe wyświetlenie:

```powerfx
Concat(
    ThisItem.Tags,
    Value,
    ", "
)
```

## 6. Lookup

Typowy odczyt:

```powerfx
ThisItem.Supplier.Id
ThisItem.Supplier.Value
```

Nie zakładaj, że Lookup zawiera cały rekord listy źródłowej. Jeżeli potrzebujesz dodatkowych pól, może być potrzebne osobne `LookUp()`.

## 7. Person or Group

Najczęstsze właściwości:

```powerfx
ThisItem.Owner.DisplayName
ThisItem.Owner.Email
ThisItem.Owner.Claims
```

Dla wielu osób wartość jest tabelą.

## 8. Date / DateTime

Odczyt:

```powerfx
ThisItem.ValidFrom
```

Formatowanie:

```powerfx
Text(
    ThisItem.ValidFrom,
    "[$-pl-PL]dd.MM.yyyy"
)
```

Przy DateTime uwzględnij ustawienia strefy czasowej SharePoint i Power Apps.

## 9. Hyperlink

Kolumna może być reprezentowana jako wartość zawierająca URL i opis, zależnie od sposobu użycia oraz kontrolki.

Przed implementacją sprawdź strukturę przez:

```powerfx
ThisItem.
```

i IntelliSense.

## 10. Attachments

Załączniki są obsługiwane głównie przez kontrolkę Attachments wewnątrz formularza SharePoint/Power Apps.

Nie traktuj ich jak zwykłej kolumny tekstowej.

Dla złożonego zarządzania dokumentami preferuj bibliotekę dokumentów.

## 11. Calculated

Kolumny obliczane są wygodne do prezentacji, ale mogą komplikować delegację i aktualizację.

Nie próbuj ich zapisywać z Power Apps.

## 12. Managed Metadata

Managed Metadata jest bardziej złożone niż Choice i wymaga dodatkowej uwagi przy zapisie, filtrowaniu i integracji.

Jeżeli aplikacja intensywnie pracuje na taxonomy, przetestuj dokładnie scenariusz delegacji i zapisu.

## 13. Internal name vs display name

SharePoint posiada nazwę wewnętrzną i nazwę wyświetlaną.

Przykład:

```text
Internal name: Title
Display name: Tytuł
```

Power Apps może pokazywać nazwę wyświetlaną, natomiast SharePoint REST i OData często wymagają internal name.

Internal name nie zmienia się po zmianie display name.

## 14. Debugowanie typu pola

Jeżeli nie wiesz, co zwraca kontrolka lub rekord:

1. wpisz `ThisItem.`,
2. sprawdź IntelliSense,
3. dodaj tymczasowy Label,
4. użyj Live Monitor,
5. sprawdź wartość w formularzu i w SharePoint.

## 15. Zasada

Nie projektuj formuł na podstawie samej nazwy kolumny. Najpierw ustal jej typ oraz strukturę wartości Power Fx.
