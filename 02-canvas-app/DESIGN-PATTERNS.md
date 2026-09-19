# Power Apps – wzorce projektowe i zasady projektowania

## Po co nam wzorce w Power Apps

Power Apps pozwala bardzo szybko zbudować działającą aplikację. Problem zaczyna się wtedy, gdy aplikacja rośnie: pojawia się więcej ekranów, więcej źródeł danych, więcej logiki Power Fx i coraz więcej zależności między kontrolkami.

Wzorce projektowe pomagają ograniczyć ten problem. Nie są celem samym w sobie. Mają sprawić, że aplikacja będzie:

- łatwiejsza do zrozumienia,
- łatwiejsza do testowania,
- łatwiejsza do rozwijania,
- bardziej wydajna,
- mniej podatna na regresje.

---

# 1. Separation of Concerns

## Idea

Rozdziel:

- UI,
- stan aplikacji,
- logikę biznesową,
- dostęp do danych,
- integrację.

Canvas App nie powinna być jednocześnie formularzem, silnikiem workflow i warstwą integracyjną.

## W VCM

Canvas App:

- wyświetla umowy,
- waliduje podstawowe dane,
- zapisuje rekord Contract,
- uruchamia zmianę stanu biznesowego.

Power Automate:

- wykonuje approvals,
- realizuje integrację HTTP,
- zapisuje log techniczny.

Dataverse:

- przechowuje stan biznesowy,
- relacje,
- historię.

## Antywzorzec

Przycisk w Canvas App:

```text
Patch(...)
-> Approval
-> HTTP
-> kilka kolejnych Patch()
-> Notify()
```

To tworzy silne sprzężenie UI z procesem backendowym.

---

# 2. Screen as a Feature

## Idea

Ekran odpowiada za jedną konkretną funkcję użytkownika.

Przykład:

```text
scrContracts
scrContractDetails
scrContractEdit
```

Nie twórz jednego ekranu z dziesiątkami paneli sterowanych przez ogromną liczbę zmiennych Visible.

## Korzyści

- prostsze formuły,
- mniejsze zależności,
- łatwiejszy debugging,
- łatwiejsza nawigacja.

---

# 3. Navigation Parameter Pattern

## Idea

Przekazuj dane pomiędzy ekranami przez parametry nawigacji zamiast odwoływać się do kontrolek na innych ekranach.

Zamiast:

```powerfx
galContracts.Selected
```

używanego na wielu ekranach, możesz zrobić:

```powerfx
Navigate(
    scrContractDetails,
    ScreenTransition.Fade,
    { ctxContract: ThisItem }
)
```

Na ekranie szczegółów:

```powerfx
ctxContract
```

## Dlaczego

Zmniejszasz zależności pomiędzy ekranami i kontrolkami.

---

# 4. State Management Pattern

## Idea

Rozróżniaj typ stanu.

### Context variables

Stan lokalny ekranu:

```powerfx
UpdateContext({ctxEditMode: true})
```

### Global variables

Stan współdzielony pomiędzy ekranami:

```powerfx
Set(varCurrentUserRole, "Admin")
```

### Collections

Lokalny zestaw danych:

```powerfx
ClearCollect(colStatuses, ...)
```

## Reguła

Nie używaj zmiennych globalnych tylko dlatego, że są wygodne.

Im szerszy zakres zmiennej, tym trudniej śledzić jej cykl życia.

---

# 5. Form Pattern

## Idea

Jeśli formularz wykonuje klasyczny CRUD, preferuj Edit Form / Display Form zamiast budowania wszystkiego ręcznie z Patch.

```text
NewForm()
EditForm()
SubmitForm()
ResetForm()
```

Patch jest dobry, gdy:

- zapisujesz dane z wielu źródeł,
- tworzysz rekord techniczny,
- potrzebujesz bardziej kontrolowanego zapisu.

## Antywzorzec

Ręczny Patch kilkunastu pól tam, gdzie standardowy formularz rozwiązuje problem czytelniej.

---

# 6. Delegation First

## Idea

Najpierw zaprojektuj zapytanie tak, aby źródło danych wykonało filtr, sortowanie i wyszukiwanie.

Nie pobieraj dużego zbioru danych do aplikacji tylko po to, aby filtrować go lokalnie.

## Dobra intencja

```powerfx
Filter(
    Contracts,
    Status = 'Contract Status'.Submitted
)
```

jeżeli formuła jest delegowalna dla danego źródła.

## Antywzorzec

```powerfx
ClearCollect(colContracts, Contracts)
```

a następnie filtrowanie całego zbioru lokalnie.

## Zasada

Brak czerwonego błędu nie oznacza, że zapytanie jest poprawnie delegowane.

---

# 7. Server-side over Client-side

## Idea

Jeżeli logika może być wykonana po stronie Dataverse, SQL, widoku lub flow – nie rób kosztownego data mashupu w Canvas App.

Przykłady problemów:

- wiele LookUp() w galerii,
- AddColumns() wywołujące zewnętrzne źródła,
- N+1 requests.

## W VCM

Supplier jest relacją Dataverse, więc korzystaj z lookupu, zamiast wykonywać osobny request po nazwie dostawcy dla każdego Contract.

---

# 8. Reusable Component Pattern

## Idea

Powtarzalne elementy interfejsu wydzielaj do komponentów.

Przykłady:

- nagłówek,
- menu,
- komunikat błędu,
- panel statusu,
- kontrolka wyszukiwania.

## Korzyść

Jedna zmiana zamiast poprawiania wielu ekranów.

---

# 9. Configuration over Hard-code

## Idea

Nie zaszywaj w Power Fx:

- adresów email,
- URL-i,
- progów biznesowych,
- nazw środowisk.

Konfiguracja powinna pochodzić z:

- Environment Variables,
- Dataverse configuration table,
- parametrów aplikacji.

## Antywzorzec

```powerfx
If(Amount > 100000, ...)
```

powielone w wielu miejscach aplikacji, jeśli próg jest elementem zmiennej polityki biznesowej.

---

# 10. Optimistic UI vs Confirmed State

## Optimistic UI

Interfejs zakłada sukces i od razu pokazuje użytkownikowi zmianę.

Dobre dla:

- prostych zapisów,
- niskiego ryzyka.

## Confirmed State

UI pokazuje status dopiero po potwierdzeniu zapisu lub procesu backendowego.

Dobre dla:

- approval,
- integracji,
- operacji finansowych,
- procesów wieloetapowych.

## VCM

Po kliknięciu Submit umowa może przejść na `Submitted`, ale nie powinna natychmiast wyglądać jak `Approved`.

---

# 11. Error Boundary Pattern

## Idea

Błąd techniczny i błąd biznesowy to dwie różne rzeczy.

Przykład:

```text
Rejected = wynik biznesowy
HTTP 500 = błąd techniczny
```

Canvas App powinna pokazać użytkownikowi komunikat zrozumiały biznesowo, a szczegóły techniczne trafić do logów.

---

# 12. Lazy Loading

## Idea

Nie ładuj wszystkiego przy starcie aplikacji.

Ładuj dane wtedy, gdy są potrzebne.

## Antywzorzec

Ogromny `App.OnStart` pobierający:

- wszystkie umowy,
- wszystkich dostawców,
- konfigurację,
- approvals,
- logi.

## Lepiej

- dane konfiguracyjne przy starcie,
- dane biznesowe per ekran,
- szczegóły po wyborze rekordu.

---

# 13. Naming Convention

Przykład:

```text
scrContracts
galContracts
frmContract
btnSaveContract
txtSearch
drpStatus
varCurrentUser
ctxContract
colStatuses
```

Nazwy techniczne mają redukować czas potrzebny na zrozumienie aplikacji.

---

# 14. Anti-patterns w Canvas Apps

Unikaj:

- jednego ogromnego ekranu,
- odwołań między kontrolkami z różnych ekranów,
- Set() dla każdej drobnej wartości,
- kolekcjonowania całych dużych tabel,
- N+1 LookUp(),
- ciężkiego App.OnStart,
- logiki biznesowej rozproszonej po OnSelect wielu kontrolek,
- hard-code środowiskowy,
- duplikowania tych samych formuł w wielu miejscach.

---

# Checklista projektowa Power Apps

Przed publikacją odpowiedz:

1. Czy każdy ekran ma jedną odpowiedzialność?
2. Czy logika biznesowa nie jest przypadkiem ukryta w UI?
3. Czy zapytania są delegowalne?
4. Czy nie pobieramy zbyt dużych zbiorów?
5. Czy nie mamy cross-screen references?
6. Czy wspólne elementy są komponentami?
7. Czy konfiguracja nie jest zaszyta w kodzie?
8. Czy użytkownik odróżnia błąd biznesowy od technicznego?
9. Czy Monitor pokazuje niepotrzebne requesty?
10. Czy nazwy kontrolek i zmiennych są jednoznaczne?

---

# Materiały Microsoft

- Power Apps coding guidelines: https://learn.microsoft.com/en-us/power-apps/guidance/coding-guidelines/overview
- App design guidelines: https://learn.microsoft.com/en-us/power-apps/guidance/coding-guidelines/app-design-guidelines
- Code optimization: https://learn.microsoft.com/en-us/power-apps/guidance/coding-guidelines/code-optimization
- Performance guidance: https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/create-performant-apps-overview
