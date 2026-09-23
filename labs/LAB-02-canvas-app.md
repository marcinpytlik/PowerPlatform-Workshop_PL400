# LAB 02 – Canvas App: rejestracja i przeglądanie umów

## Cel laboratorium

Zbudować Canvas App `VCM - Contract Portal`, która korzysta z list SharePoint utworzonych w LAB 01.

Po ukończeniu uczestnik potrafi:

- utworzyć Canvas App,
- dodać źródła danych SharePoint,
- zbudować galerię umów,
- filtrować i wyszukiwać dane,
- utworzyć formularz dodawania i edycji,
- wykonywać walidację w Power Fx,
- użyć `Notify()`, `SubmitForm()` i `Trace()`,
- rozpoznać ostrzeżenia delegacji.

## Czas

75–90 minut.

## Wymagania

Ukończony LAB 01.

---

# Zadanie 1 – Utworzenie aplikacji

1. Otwórz `https://make.powerapps.com`.
2. Upewnij się, że wybrane jest właściwe środowisko.
3. Wybierz **Create / Utwórz**.
4. Utwórz **Canvas app** w układzie responsywnym lub tabletowym.
5. Nazwa: `VCM - Contract Portal`.
6. Zapisz aplikację.

> W tenantcie jest nowszy start z danych, można również utworzyć Canvas App na podstawie listy `Contracts`, ale podczas szkolenia rozpocznij od pustej aplikacji – uczestnik lepiej widzi architekturę.

---

# Zadanie 2 – Dodanie źródeł danych

1. W lewym menu wybierz **Data / Dane**.
2. **Add data / Dodaj dane**.
3. Wybierz connector **SharePoint**.
4. Wskaż witrynę szkoleniową.
5. Dodaj:
   - `Contracts`,
   - `Suppliers`,
   - `ContractApprovals`.

Sprawdź, czy wszystkie trzy źródła są widoczne w panelu Data.

## Ważne: sharing aplikacji a dostęp do SharePoint

Udostępnienie Canvas App nie nadaje automatycznie uprawnień do list SharePoint.

Dla bezpośredniego modelu:

```text
Canvas App -> SharePoint
```

użytkownik końcowy pracuje na danych zgodnie ze swoimi uprawnieniami SharePoint. Connection developera nie powoduje impersonacji użytkowników.

Przykład:

```text
Heniek udostępnia aplikację Marcinowi
!=
Marcin automatycznie dostaje dostęp do Contracts
```

Jeżeli Marcin ma korzystać bezpośrednio z `Contracts`, `Suppliers` i `ContractApprovals`, trzeba nadać mu odpowiednie uprawnienia do tych źródeł.

Konto techniczne, np. `aplikacjaSharePoint`, ma sens dopiero wtedy, gdy operacje wykonuje warstwa pośrednia:

```text
Canvas App
   |
   v
Power Automate
   |
   v
SharePoint connection konta technicznego
```

Jeżeli użytkownik **nie powinien mieć bezpośredniego dostępu do listy**, nie projektuj galerii jako `Gallery.Items = Contracts`. Wtedy odczyty i zapisy również trzeba przenieść do kontrolowanej warstwy pośredniej.

---

# Zadanie 3 – Ekran listy umów

1. Zmień nazwę pierwszego ekranu na `scrContracts`.
2. Dodaj nagłówek Label:

```text
Vendor Contract Management
```

3. Dodaj Text Input i zmień nazwę na `txtSearch`.
4. Ustaw HintText:

```text
Szukaj numeru umowy...
```

5. Dodaj Dropdown/Combo box do filtrowania statusów. Nazwa: `drpStatus`.
6. Ustaw `Items` kontrolki statusu:

```powerfx
["All", "Draft", "Submitted", "In Approval", "Approved", "Rejected", "Integration Pending", "Integrated", "Integration Error"]
```

7. Dodaj **Vertical gallery** i nazwij `galContracts`.

## Items galerii

Na początek ustaw:

```powerfx
SortByColumns(
    Filter(
        Contracts,
        (drpStatus.Selected.Value = "All" || Status.Value = drpStatus.Selected.Value) &&
        (IsBlank(txtSearch.Text) || StartsWith(Title, txtSearch.Text))
    ),
    "Title",
    SortOrder.Ascending
)
```

> Jeśli kontrolka statusu zwraca `SelectedText.Value` albo inną właściwość, dopasuj formułę do typu kontrolki. Celem ćwiczenia jest zrozumienie filtra, nie zapamiętanie jednej wersji kontrolki.
>
> W nowych kontrolkach tekstowych Power Apps właściwość wpisanej wartości może być `.Value` zamiast `.Text`. Jeżeli filtr zwraca pustą galerię mimo poprawnych danych, sprawdź właściwość kontrolki `txtSearch`. Przykład dla modern Text Input:
>
> ```powerfx
> IsBlank(txtSearch.Value) || StartsWith(Title, txtSearch.Value)
> ```

W galerii pokaż:

- numer umowy,
- dostawcę,
- kwotę i walutę,
- status,
- datę końca.

Przykładowe Text dla etykiet:

```powerfx
ThisItem.Title
```

```powerfx
ThisItem.Supplier.Value
```

```powerfx
Text(ThisItem.Amount, "#,##0.00") & " " & ThisItem.Currency.Value
```

> Uwaga na nazwy kolumn SharePoint. `Title` jest nazwą wewnętrzną, ale w polskim interfejsie Power Apps pole może być prezentowane jako `Tytuł`. Jeżeli `ThisItem.Title` nie jest rozpoznawane, sprawdź podpowiedzi IntelliSense i użyj właściwości widocznej dla danego źródła, np. `ThisItem.Tytuł`.
>
> Kolumny wyświetlane w galerii są właściwościami kontrolek wewnątrz template galerii. Nie dodaje się ich jako kolejnych argumentów do `SortByColumns()`. Przykładowo trzy etykiety mogą mieć odpowiednio:
>
> ```powerfx
> ThisItem.Tytuł
> ThisItem.Supplier.Value
> ThisItem.Status.Value
> ```

---

# Zadanie 4 – Oznaczenie umów wygasających

Dodaj do szablonu galerii ikonę ostrzeżenia lub Label.

Ustaw `Visible`:

```powerfx
ThisItem.ValidTo >= Today() && ThisItem.ValidTo <= DateAdd(Today(), 30, TimeUnit.Days)
```

Tekst:

```text
Wygasa <= 30 dni
```

Dla umów już wygasłych dodaj drugi komunikat:

```powerfx
ThisItem.ValidTo < Today()
```

---

# Zadanie 5 – Ekran szczegółów

1. Dodaj nowy ekran `scrContractDetails`.
2. Dodaj Display Form `frmContractDetails`.
3. DataSource: `Contracts`.
4. Item:

```powerfx
galContracts.Selected
```

5. Dodaj pola:
   - Title/ContractNumber,
   - Supplier,
   - Amount,
   - Currency,
   - ValidFrom,
   - ValidTo,
   - Status,
   - ExternalSystemId,
   - CorrelationId.

6. Na `OnSelect` rekordu w galerii ustaw:

```powerfx
Navigate(scrContractDetails, ScreenTransition.Fade)
```

Szczegóły biorą `galContracts.Selected`. To jest celowo prostsze niż Navigation Parameter z [DESIGN-PATTERNS](../02-canvas-app/DESIGN-PATTERNS.md). Nie przepisuj labu w dniu 1.

---

# Zadanie 6 – Formularz nowej umowy

1. Dodaj ekran `scrContractEdit`.
2. Dodaj Edit Form `frmContract`.
3. DataSource: `Contracts`.
4. Dodaj wymagane pola.
5. Dodaj przycisk `Nowa umowa` na ekranie listy.
6. `OnSelect`:

```powerfx
NewForm(frmContract);
Navigate(scrContractEdit, ScreenTransition.Cover)
```

## Przycisk Zapisz

Dodaj button `btnSaveContract`.

Przykładowa walidacja dla klasycznych kontrolek:

```powerfx
If(
    IsBlank(DataCardValue_ContractNumber.Text),
    Notify("Podaj numer umowy", NotificationType.Error),
    IsBlank(DataCardValue_Supplier.Selected),
    Notify("Wybierz dostawcę", NotificationType.Error),
    Value(DataCardValue_Amount.Text) <= 0,
    Notify("Kwota musi być większa od 0", NotificationType.Error),
    DataCardValue_ValidTo.SelectedDate < DataCardValue_ValidFrom.SelectedDate,
    Notify("Data końca nie może być wcześniejsza od daty początku", NotificationType.Error),
    SubmitForm(frmContract)
)
```

Dla modern controls Text Input często używa `.Value`, a nie `.Text`. Przykład:

```powerfx
If(
    IsBlank(Trim(DataCardValue_ContractNumber.Value)),
    Notify("Podaj numer umowy", NotificationType.Error),
    IsBlank(DataCardValue_Supplier.Selected.Value),
    Notify("Wybierz dostawcę", NotificationType.Error),
    IsBlank(DataCardValue_Amount.Value) || Value(DataCardValue_Amount.Value) <= 0,
    Notify("Kwota musi być większa od 0", NotificationType.Error),
    SubmitForm(frmContract)
)
```

Nazwy `DataCardValue_*` i właściwości kontrolek dostosuj do kontrolek utworzonych w Twojej aplikacji.

Jeżeli formularz ma poprawnie skonfigurowane pola Required, można też wykorzystać:

```powerfx
frmContract.Valid
```

jako część walidacji, zamiast ręcznie powielać wszystkie reguły wymaganych pól.

## OnSuccess formularza

Ustaw:

```powerfx
Notify("Umowa została zapisana", NotificationType.Success);
Trace(
    "Contract saved",
    TraceSeverity.Information,
    { ContractNumber: frmContract.LastSubmit.Title }
);
Navigate(scrContracts, ScreenTransition.Fade)
```

## OnFailure

```powerfx
Notify(
    "Nie udało się zapisać umowy: " & frmContract.Error,
    NotificationType.Error
)
```

---

# Zadanie 7 – Edycja umowy

Na `scrContractDetails` dodaj przycisk `Edytuj`:

```powerfx
EditForm(frmContract);
Navigate(scrContractEdit, ScreenTransition.Cover)
```

Ustaw `Item` formularza:

```powerfx
galContracts.Selected
```

---

# Zadanie 8 – Odświeżanie danych

Dodaj ikonę Refresh na `scrContracts`.

```powerfx
Refresh(Contracts);
Notify("Dane odświeżone", NotificationType.Information)
```

---

# Zadanie 9 – Delegation check

1. Zaznacz formułę `Items` galerii.
2. Sprawdź, czy Power Apps pokazuje niebieskie ostrzeżenie delegacji.
3. Jeżeli występuje:
   - zidentyfikuj niedelegowalny fragment,
   - zastanów się, czy `StartsWith()` lub filtr statusu może zostać wykonany u źródła,
   - nie rozwiązuj problemu przez `ClearCollect(Contracts)` dla całej listy.

Zapisz obserwację w notatkach uczestnika.

---

# Test końcowy

1. Uruchom Preview aplikacji.
2. Wyszukaj `VCM/2026/002`.
3. Ustaw filtr `Submitted`.
4. Otwórz szczegóły.
5. Edytuj kwotę.
6. Zapisz.
7. Utwórz nową umowę.
8. Spróbuj zapisać formularz bez numeru – walidacja ma zablokować zapis.
9. Utwórz poprawny rekord.
10. Sprawdź listę SharePoint.

## Kryterium ukończenia

- aplikacja ma trzy ekrany,
- można przeglądać, dodawać i edytować umowy,
- działa filtr statusu i wyszukiwanie,
- walidacja pokazuje `Notify`,
- umowy wygasające są oznaczone,
- uczestnik potrafi wskazać miejsce sprawdzania delegacji.

## Po tym LAB

Talk track: Separation of Concerns, Screen as a Feature, Delegation First. Szczegóły: [THEORY-TALK-TRACK](../trainer/THEORY-TALK-TRACK.md).

---

# Challenge

Dodaj pole `My contracts` i filtruj listę do rekordów, gdzie:

```powerfx
RequestorEmail = User().Email
```

Następnie sprawdź delegację tej formuły dla SharePoint.

---

# Materiał Microsoft

- Create a canvas app with data from a SharePoint list: https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/app-from-sharepoint
- Patch function: https://learn.microsoft.com/en-us/power-platform/power-fx/reference/function-patch
