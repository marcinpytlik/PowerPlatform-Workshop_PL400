# SharePoint Online, Power Apps i Power Automate – bezpieczeństwo i połączenia

## Cel dokumentu

Dokument opisuje różnice pomiędzy uprawnieniami użytkownika, sharingiem aplikacji oraz kontami używanymi przez connection w Power Automate.

## 1. Power Apps i kontekst użytkownika

Canvas App korzystająca bezpośrednio z SharePoint zwykle działa w kontekście użytkownika.

Użytkownik musi mieć odpowiednie uprawnienia do źródła danych.

Samo udostępnienie aplikacji nie oznacza automatycznie udostępnienia wszystkich źródeł danych.

## 2. Sharing aplikacji vs sharing SharePoint

To dwa różne mechanizmy.

```text
App shared
!=
SharePoint permissions granted
```

Użytkownik może mieć dostęp do aplikacji, ale nie do listy, z której aplikacja korzysta.

## 3. Power Automate i connection owner

Flow może wykonywać akcje przez connection należące do określonego konta.

To oznacza, że flow może mieć większe uprawnienia niż użytkownik inicjujący proces.

Taki model może być poprawny, ale musi być świadomie zaprojektowany.

## 4. Service account / technical identity

Współdzielone procesy nie powinny bez potrzeby zależeć od prywatnego konta developera.

Ryzyka:

- odejście użytkownika,
- wygasłe hasło,
- odebrane licencje,
- zmiana MFA,
- brak właściciela procesu.

## 5. Least privilege

Connection techniczne powinno mieć minimalny zestaw wymaganych uprawnień.

Nie należy przyznawać Full Control tylko dlatego, że upraszcza development.

## 6. Item-level permissions

Indywidualne uprawnienia elementów są możliwe, ale zwiększają liczbę security scopes.

Przy dużej liczbie rekordów model może stać się kosztowny.

## 7. Broken inheritance

Łamanie dziedziczenia dla tysięcy rekordów wymaga ostrożności.

Lepszym modelem może być:

- podział danych,
- folder-level permissions,
- osobne listy,
- Dataverse security,
- inny model domenowy.

## 8. "Run-only users"

Przy flowach wywoływanych ręcznie trzeba rozumieć, czy akcje korzystają z connection właściciela czy użytkownika uruchamiającego.

Model powinien być spójny z wymaganiami bezpieczeństwa.

## 9. Connection References

W Solution connection powinny być reprezentowane przez Connection References.

Pozwala to odłączyć lifecycle rozwiązania od prywatnego connection developera.

## 10. DLP

Data Loss Prevention Policies mogą ograniczać:

- HTTP,
- custom connectors,
- łączenie connectorów Business i Non-Business,
- użycie wybranych usług.

Błąd aplikacji lub flow może więc wynikać z polityki środowiska, a nie z samego kodu.

## 11. Sekrety

Sekretów nie należy przechowywać:

- w Power Fx,
- w zwykłych zmiennych tekstowych,
- w bundle SPFx,
- w komentarzach,
- w opisach flow.

## 12. Audyt

SharePoint version history i auditing Power Platform rozwiązują inne problemy.

Warto rozdzielić:

- kto zmienił rekord,
- jaki flow wykonał operację,
- jakie connection zostało użyte,
- jaki był correlation ID.

## 13. Checklista

- Czy użytkownik ma dostęp do źródła danych?
- Czy sharing aplikacji jest zgodny z uprawnieniami SharePoint?
- Na czyim connection działa flow?
- Czy proces zależy od prywatnego konta?
- Czy connection ma minimalne uprawnienia?
- Czy item-level permissions nie rosną nadmiernie?
- Czy DLP pozwala na wymagane connectory?


## 14. Udostępnienie Canvas App korzystającej z listy SharePoint

Jeżeli Canvas App korzysta bezpośrednio z listy SharePoint, trzeba rozdzielić dwa niezależne poziomy dostępu:

```text
1. dostęp do aplikacji Power Apps
2. dostęp do danych w SharePoint
```

Udostępnienie aplikacji użytkownikowi nie nadaje automatycznie uprawnień do listy SharePoint.

Typowy model:

```text
User
  |
  +--> ma udostępnioną Canvas App
  |
  +--> uwierzytelnia się swoim kontem do SharePoint
  |
  +--> SharePoint sprawdza jego rzeczywiste uprawnienia do listy
```

To, że developer utworzył connection do SharePoint podczas budowania aplikacji, nie oznacza, że każdy użytkownik aplikacji wykonuje operacje na uprawnieniach developera.

Dla bezpośredniego connectora SharePoint użytkownik powinien mieć własny dostęp do danych wymaganych przez aplikację.

## 15. Jak nadać użytkownikom aplikacji dostęp do listy

Najbezpieczniej zarządzać dostępem grupowo zamiast nadawać uprawnienia pojedynczym osobom.

Przykładowy model:

```text
Microsoft 365 / Entra ID / SharePoint Group
        |
        +--> użytkownicy aplikacji
        |
        +--> uprawnienia do witryny lub listy SharePoint
```

Jeżeli użytkownicy mogą edytować rekordy, potrzebują co najmniej uprawnień pozwalających na odpowiednie operacje na elementach listy.

W praktyce można zastosować jeden z dwóch modeli.

### Model A – uprawnienia dziedziczone z witryny

Użytkownik lub grupa jest dodana do odpowiedniej grupy witryny, np. Members.

```text
SharePoint Site
   |
   +--> Members
          |
          +--> użytkownicy aplikacji
```

Lista dziedziczy uprawnienia z witryny.

Zalety:

- prostszy lifecycle,
- mniej wyjątków,
- łatwiejszy audyt,
- mniejsze ryzyko rozrostu unikalnych security scopes.

### Model B – uprawnienia tylko do konkretnej listy

Jeżeli użytkownik nie powinien mieć szerszego dostępu do witryny, można zatrzymać dziedziczenie uprawnień na liście i nadać dostęp dedykowanej grupie.

Przykład:

```text
Site
 |
 +--> Contracts
        |
        +--> VCM-App-Users
               |
               +--> Edit / Contribute
```

Taki model powinien być stosowany świadomie, ponieważ zwiększa liczbę miejsc z niestandardowym modelem bezpieczeństwa.

## 16. Co dzieje się po udostępnieniu aplikacji

Typowy proces wdrożenia wygląda następująco:

1. Udostępnić Canvas App użytkownikowi lub grupie.
2. Nadać tej samej grupie wymagane uprawnienia do SharePoint.
3. Użytkownik uruchamia aplikację.
4. Power Apps zestawia wymagane połączenie do SharePoint w kontekście użytkownika.
5. SharePoint autoryzuje każdą operację zgodnie z uprawnieniami tego użytkownika.

Jeżeli użytkownik ma dostęp do aplikacji, ale nie ma dostępu do listy, aplikacja może się uruchomić, ale operacje na danych będą kończyć się błędami lub zwracać brak danych.

## 17. Connection developera nie jest mechanizmem autoryzacji aplikacji

Connection utworzone podczas developmentu służy developerowi do pracy ze źródłem danych.

Nie należy projektować aplikacji w założeniu:

```text
"Skoro moje connection ma dostęp do listy,
to każdy użytkownik aplikacji też będzie miał dostęp."
```

Dla bezpośredniej komunikacji Canvas App -> SharePoint właściwy model to:

```text
Canvas App
    |
    +--> użytkownik A --> jego uprawnienia SharePoint
    +--> użytkownik B --> jego uprawnienia SharePoint
    +--> użytkownik C --> jego uprawnienia SharePoint
```

SharePoint pozostaje warstwą autoryzującą dostęp do danych.

## 18. Konto techniczne nie zastępuje użytkownika przy bezpośrednim połączeniu Canvas App -> SharePoint

To jest kluczowa różnica architektoniczna.

Jeżeli Canvas App ma bezpośrednio dodane źródło danych SharePoint:

```text
Marcin
   |
   v
Canvas App
   |
   v
SharePoint connector
   |
   v
Contracts
```

to operacje na liście są autoryzowane zgodnie z uprawnieniami Marcina.

Nie ma w Canvas App ustawienia, w którym można wpisać konto:

```text
aplikacjaSharepoint@firma.pl
```

i sprawić, żeby każdy zalogowany użytkownik wykonywał bezpośrednie operacje SharePoint jako to konto.

Nie należy też umieszczać loginu ani hasła konta technicznego w Power Fx.

Jeżeli galeria korzysta z:

```powerfx
Gallery.Items = Contracts
```

to użytkownik aplikacji musi mieć wymagane uprawnienia do listy `Contracts`.

Connection używane przez developera podczas budowania aplikacji nie jest mechanizmem impersonacji użytkowników końcowych.

## 19. Kiedy konto techniczne ma zastosowanie

Konto techniczne ma zastosowanie wtedy, gdy operacja na SharePoint jest wykonywana przez warstwę pośrednią, np. Power Automate.

Przykład:

```text
Marcin
   |
   v
Canvas App
   |
   v
Power Automate
   |
   v
SharePoint connection
konto: aplikacjaSharepoint
   |
   v
Contracts
```

W takim modelu:

1. użytkownik loguje się do Canvas App swoim kontem,
2. aplikacja wywołuje flow,
3. flow wykonuje akcje SharePoint przez skonfigurowane connection,
4. connection może należeć do dedykowanej tożsamości technicznej.

To rozdziela:

```text
tożsamość użytkownika aplikacji
od
tożsamości wykonującej operację backendową
```

Ma to sens dla kontrolowanych operacji technicznych, np.:

- generowanie dokumentu,
- integracja z API,
- zapis technicznego statusu,
- centralny zapis logu,
- operacja wymagająca dodatkowych uprawnień.

Nie należy jednak używać konta technicznego jako prostego sposobu na obejście całego modelu bezpieczeństwa SharePoint.

Jeżeli flow wykonuje operację w imieniu użytkownika, powinien sam sprawdzać, czy użytkownik ma prawo uruchomić daną operację.

## 20. Jeżeli użytkownik nie ma mieć bezpośredniego dostępu do listy

Jeżeli wymaganie brzmi:

```text
Użytkownik może korzystać z aplikacji,
ale nie powinien mieć bezpośrednich uprawnień do listy SharePoint.
```

to aplikacja nie powinna korzystać z listy bezpośrednio.

Zamiast:

```text
Canvas App
   |
   v
SharePoint
```

należy zastosować np.:

```text
Canvas App
   |
   +--> Flow_GetContracts
   +--> Flow_CreateContract
   +--> Flow_UpdateContract
   +--> Flow_DeleteContract
              |
              v
       konto techniczne
              |
              v
          SharePoint
```

W takim modelu galeria nie pracuje bezpośrednio na źródle `Contracts`, lecz np. na kolekcji zwróconej przez flow.

Przykład koncepcyjny:

```powerfx
ClearCollect(
    colContracts,
    Flow_GetContracts.Run()
)
```

a następnie:

```powerfx
Gallery.Items = colContracts
```

Taki model ma większy koszt implementacyjny i trzeba świadomie zaprojektować autoryzację po stronie flow.

## 21. Zalecany model dla typowej aplikacji Canvas + SharePoint

Dla typowej aplikacji biznesowej, w której użytkownik może bezpośrednio pracować z listami SharePoint:

```text
Entra ID / Microsoft 365 Group
        |
        +--> Share Canvas App
        |
        +--> SharePoint permissions
```

Przykład:

```text
VCM-App-Users
    |
    +--> Power Apps: User
    |
    +--> SharePoint Contracts: Contribute
    |
    +--> SharePoint Suppliers: Read
```

Dzięki temu użytkownik działa na SharePoint własną tożsamością, a dodanie nowej osoby sprowadza się do zarządzania członkostwem w grupie.

Konto techniczne warto zostawić dla operacji backendowych wykonywanych przez flow, a nie dla zwykłego odczytu i edycji listy bezpośrednio przez Canvas App.

## 19. Zalecany model dla aplikacji Canvas + SharePoint

Dla typowej aplikacji biznesowej:

```text
Entra ID / M365 Group
        |
        +--> Share Canvas App
        |
        +--> SharePoint permissions
```

Przykład:

```text
VCM-App-Users
    |
    +--> Power Apps: User
    |
    +--> SharePoint Contracts: Contribute
    |
    +--> SharePoint Suppliers: Read
```

Dzięki temu dodanie nowego użytkownika oznacza zmianę członkostwa w jednej grupie zamiast ręcznej konfiguracji kilku zasobów.

## 22. Przykład minimalnych uprawnień

Załóżmy aplikację VCM korzystającą z:

```text
Contracts
Suppliers
ProcessLog
```

Można zaprojektować dostęp:

| Lista | Uprawnienie użytkownika |
|---|---|
| Contracts | odczyt + dodawanie + edycja |
| Suppliers | odczyt |
| ProcessLog | brak bezpośredniego dostępu albo tylko odczyt |
| konfiguracja techniczna | brak |

Jeżeli zapis do ProcessLog wykonuje wyłącznie flow techniczny, użytkownik aplikacji nie musi mieć prawa zapisu do tej listy.

To jest przykład zastosowania zasady least privilege.

## 23. Test bezpieczeństwa po udostępnieniu aplikacji

Nie należy testować aplikacji wyłącznie na koncie developera lub właściciela witryny.

Minimalny test powinien obejmować konto zwykłego użytkownika:

```text
Test User
    |
    +--> app shared: YES
    +--> site owner: NO
    +--> list permissions: zgodne z rolą
```

Należy sprawdzić:

- odczyt danych,
- tworzenie rekordów,
- edycję,
- usuwanie, jeżeli aplikacja je obsługuje,
- dostęp do Lookup / Person / Choice,
- upload załączników lub dokumentów,
- wywołanie flow,
- zachowanie po odebraniu uprawnień.

Test na koncie właściciela może ukryć problemy z bezpieczeństwem, ponieważ owner posiada znacznie szersze uprawnienia niż użytkownik końcowy.

## 24. Anti-pattern

Niepoprawny model:

```text
Developer jest właścicielem wszystkiego
        |
        +--> jego connection
        +--> jego flow
        +--> jego konto ma Full Control
        +--> użytkownicy dostają tylko link do aplikacji
```

Problemy:

- zależność od jednej osoby,
- trudny audyt,
- nadmiarowe uprawnienia,
- problemy po odejściu developera,
- możliwe obejście modelu bezpieczeństwa,
- problemy z ALM.

Lepszy model:

```text
Canvas App -> SharePoint
    = użytkownik ma własne uprawnienia do listy

Canvas App -> Power Automate -> SharePoint
    = kontrolowana operacja backendowa może używać konta technicznego
```

oraz:

```text
Groups
+ least privilege
+ application sharing
+ SharePoint permissions
+ technical identity tylko tam, gdzie jest potrzebne
+ Connection References dla flow w Solution
```

## 25. Szybka macierz decyzyjna

| Scenariusz | Czy użytkownik potrzebuje praw do listy? | Czy konto techniczne może wykonać operację? |
|---|---:|---:|
| Canvas App bezpośrednio czyta SharePoint | Tak | Nie zastępuje użytkownika |
| Canvas App bezpośrednio zapisuje do SharePoint | Tak | Nie zastępuje użytkownika |
| Canvas App wywołuje flow, a flow zapisuje do SharePoint | Nie zawsze | Tak |
| Flow działa cyklicznie / event-driven | Nie dotyczy | Tak |
| Użytkownik nie może mieć bezpośredniego dostępu do listy | Nie | Wymagana warstwa pośrednia |
