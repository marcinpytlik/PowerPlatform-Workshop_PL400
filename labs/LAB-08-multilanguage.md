# LAB 08 – Wielojęzyczny Canvas App: PL / EN / DE

## Cel laboratorium

Dodać wielojęzyczność do Canvas App bez kopiowania ekranów i bez umieszczania warunków `If(Language()=...)` w każdej kontrolce.

## Czas

60 minut.

## Wymagania

- Canvas App z LAB 02,
- plik `07-multilanguage/translations.csv`.

---

# Docelowy wzorzec

```text
UI Control
    |
    v
Translation Key
    |
    v
Translation collection/table
    |
    +-- PL
    +-- EN
    +-- DE
```

---

# Zadanie 1 – Sprawdzenie słownika

Otwórz `translations.csv` i sprawdź strukturę.

Docelowo słownik powinien zawierać klucz i tłumaczenia, np.:

```text
Key,PL,EN,DE
APP_TITLE,Zarządzanie umowami,Contract Management,Vertragsverwaltung
SAVE,Zapisz,Save,Speichern
CANCEL,Anuluj,Cancel,Abbrechen
NEW_CONTRACT,Nowa umowa,New contract,Neuer Vertrag
```

Dodaj brakujące klucze wymagane przez Twój Canvas App.

---

# Zadanie 2 – Ustawienie języka

W `App.OnStart` ustaw:

```powerfx
Set(varLanguage, Lower(Left(Language(), 2)))
```

Dodaj zabezpieczenie fallback:

```powerfx
If(
    !(varLanguage in ["pl", "en", "de"]),
    Set(varLanguage, "en")
)
```

> Funkcja `Language()` zwraca ustawienia językowe użytkownika/hosta. Nie zakładaj, że zawsze otrzymasz tylko dwuliterowy kod – dlatego pobieramy pierwsze dwa znaki.

---

# Zadanie 3 – Załadowanie tłumaczeń

Wariant A – import CSV jako dane statyczne lub kolekcja szkoleniowa.

Dla prostego LAB możesz utworzyć kolekcję w `App.OnStart`:

```powerfx
ClearCollect(
    colTranslations,
    {Key:"APP_TITLE", pl:"Zarządzanie umowami", en:"Contract Management", de:"Vertragsverwaltung"},
    {Key:"SAVE", pl:"Zapisz", en:"Save", de:"Speichern"},
    {Key:"CANCEL", pl:"Anuluj", en:"Cancel", de:"Abbrechen"},
    {Key:"NEW_CONTRACT", pl:"Nowa umowa", en:"New contract", de:"Neuer Vertrag"},
    {Key:"SEARCH", pl:"Szukaj", en:"Search", de:"Suchen"}
)
```

Wariant B – źródło konfiguracyjne SharePoint/Dataverse.

Omów, kiedy tłumaczenia powinny być utrzymywane jako dane, a nie zakodowane w aplikacji.

---

# Zadanie 4 – Mechanizm pobierania tekstu

W Canvas App nie tworzymy osobnej funkcji w każdym tenantcie w identyczny sposób; dla czytelności ćwiczenia użyjemy `Switch` bezpośrednio wokół jednego Lookup.

Przykład Text dla tytułu:

```powerfx
With(
    {tr: LookUp(colTranslations, Key = "APP_TITLE")},
    Switch(
        varLanguage,
        "pl", tr.pl,
        "de", tr.de,
        tr.en
    )
)
```

Wprowadź ten wzorzec dla przycisku Save:

```powerfx
With(
    {tr: LookUp(colTranslations, Key = "SAVE")},
    Switch(varLanguage, "pl", tr.pl, "de", tr.de, tr.en)
)
```

---

# Zadanie 5 – Przełącznik języka

Dodaj dropdown `drpLanguage`.

Items:

```powerfx
["PL", "EN", "DE"]
```

OnChange:

```powerfx
Set(varLanguage, Lower(drpLanguage.Selected.Value))
```

Default zależnie od wersji kontrolki ustaw tak, aby odzwierciedlał `Upper(varLanguage)`.

---

# Zadanie 6 – Podmiana tekstów

Podmień co najmniej:

- tytuł aplikacji,
- `Nowa umowa`,
- `Zapisz`,
- `Anuluj`,
- placeholder wyszukiwania,
- etykiety Status, Supplier, Amount,
- komunikat walidacji.

Przykład komunikatu:

```powerfx
Notify(
    With(
        {tr: LookUp(colTranslations, Key = "VALIDATION_REQUIRED")},
        Switch(varLanguage, "pl", tr.pl, "de", tr.de, tr.en)
    ),
    NotificationType.Error
)
```

---

# Zadanie 7 – Fallback

Dodaj do słownika klucz, dla którego brakuje tłumaczenia DE.

Zmień formułę tak, aby:

1. najpierw próbowała języka użytkownika,
2. jeżeli tłumaczenie jest puste – używała English,
3. jeżeli klucz nie istnieje – pokazywała techniczny marker:

```text
[[MISSING:KEY]]
```

Przykładowy wzorzec możesz zbudować z `Coalesce()` i `If(IsBlank(...))`.

---

# Zadanie 8 – Nie tłumacz danych biznesowych w UI

Omów różnicę:

```text
UI label: Status -> tłumaczymy
Business value: Approved -> zależy od modelu danych
```

Jeżeli Choice przechowuje etykiety lokalizowane przez Dataverse, wykorzystaj możliwości platformy. Jeżeli źródłem jest SharePoint i status jest tekstem/Choice, ustal stabilne wartości biznesowe i warstwę prezentacji.

---

# Test końcowy

1. Uruchom aplikację.
2. Wybierz PL.
3. Przejdź po wszystkich ekranach.
4. Wybierz EN.
5. Ponownie sprawdź wszystkie etykiety.
6. Wybierz DE.
7. Wywołaj walidację formularza.
8. Sprawdź fallback dla brakującego tłumaczenia.

---

# Kryterium ukończenia

- jeden ekran obsługuje trzy języki,
- nie ma kopii ekranów PL/EN/DE,
- istnieje centralny słownik,
- istnieje fallback,
- język można przełączyć bez restartu aplikacji.

---

# Challenge

Przenieś słownik do Dataverse i dodaj kolumny:

```text
Translation Key
Language Code
Value
Active
```

Porównaj ten znormalizowany model z modelem „jedna kolumna na język”.
