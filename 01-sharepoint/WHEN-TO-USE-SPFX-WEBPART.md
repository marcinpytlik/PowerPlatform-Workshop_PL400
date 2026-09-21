# Kiedy stosować własny webpart w SharePoint Online

## Cel dokumentu

Dokument opisuje, kiedy warto użyć własnego komponentu opartego o SharePoint Framework (SPFx), kiedy lepszym wyborem jest Power Apps, a kiedy rozwiązanie powinno być zbudowane jako niezależna aplikacja webowa.

Najważniejsze rozróżnienie:

> **Power Apps służy przede wszystkim do budowania aplikacji biznesowych. SPFx służy przede wszystkim do rozszerzania doświadczenia SharePoint.**

---

# 1. Czym jest SPFx

SharePoint Framework (SPFx) jest rekomendowanym modelem rozszerzania nowoczesnego SharePoint Online.

Pozwala budować komponenty klienckie, najczęściej w:

```text
TypeScript
React
JavaScript
```

Rozwiązania SPFx są pakowane jako:

```text
.sppkg
```

i wdrażane przez App Catalog.

SPFx może być używany do budowania:

- webpartów,
- rozszerzeń list i bibliotek,
- własnych komend,
- niestandardowego renderowania pól,
- rozszerzeń interfejsu SharePoint,
- niestandardowych formularzy.

Dokumentacja:
- SPFx overview: https://learn.microsoft.com/en-us/sharepoint/dev/spfx/sharepoint-framework-overview
- Client-side web parts: https://learn.microsoft.com/en-us/sharepoint/dev/spfx/web-parts/overview-client-side-web-parts
- SPFx Extensions: https://learn.microsoft.com/en-us/sharepoint/dev/spfx/extensions/overview-extensions

---

# 2. Kiedy SPFx ma sens

SPFx jest dobrym wyborem, gdy:

- głównym miejscem pracy użytkownika jest SharePoint,
- standardowe webparty nie wystarczają,
- wymagany jest niestandardowy UX,
- rozwiązanie ma reagować na kontekst bieżącej witryny,
- potrzebne są własne akcje na listach lub bibliotekach,
- potrzebna jest integracja z Microsoft Graph lub własnym API,
- zespół akceptuje klasyczny model developmentu i utrzymania kodu.

Typowe scenariusze:

```text
custom dashboard
niestandardowy grid
drag & drop
własny toolbar
akcje na zaznaczonych dokumentach
niestandardowy formularz
własny rendering pola
integracja z kontekstem strony
```

---

# 3. SPFx jako rozszerzenie SharePoint

SPFx najlepiej pasuje do sytuacji, w której SharePoint pozostaje główną powierzchnią użytkownika.

Przykład:

```text
SharePoint Portal
   |
   +--> standardowa nawigacja
   +--> biblioteki dokumentów
   +--> listy
   +--> własny SPFx dashboard
```

W takim modelu SPFx nie zastępuje SharePoint, tylko rozszerza jego interfejs.

---

# 4. Przykład: dashboard VCM

Dla Vendor Contract Management można zbudować webpart prezentujący dane bezpośrednio na stronie SharePoint:

```text
Moje umowy

Draft                 4
In Approval            3
Rejected               1
Integrated            12

[Nowa umowa]

Ostatnie umowy
--------------------------------
VCM-1001   Approved
VCM-1002   In Approval
VCM-1003   Integrated
```

Taki komponent może:

- korzystać z kontekstu bieżącego użytkownika,
- pobierać dane z SharePoint,
- pobierać dane z Dataverse,
- komunikować się z własnym API,
- wyświetlać dane w niestandardowy sposób,
- działać bezpośrednio w portalu SharePoint.

---

# 5. Kiedy Power Apps jest lepsze

Power Apps jest naturalnym wyborem, gdy rozwiązanie ma charakter aplikacji biznesowej.

Typowe wymagania:

- formularze,
- CRUD,
- kilka ekranów,
- walidacja,
- workflow,
- obsługa procesu użytkownika,
- integracja z konektorami.

Przykład:

```text
New Contract
Edit Contract
Submit
Approve
View Status
```

W takim przypadku Power Apps zwykle pozwala dostarczyć rozwiązanie szybciej i przy mniejszym koszcie utrzymania niż własny frontend SPFx.

---

# 6. Kiedy SPFx zaczyna wygrywać z Power Apps

SPFx daje przewagę, gdy potrzebna jest większa kontrola nad frontendem.

Przykłady:

- zaawansowany grid,
- niestandardowy layout,
- drag & drop,
- złożone komponenty React,
- własne menu kontekstowe,
- wyspecjalizowane wizualizacje,
- bardzo precyzyjna kontrola zachowania UI,
- integracja z elementami strony SharePoint.

Power Apps działa w modelu platformy low-code.

SPFx daje klasyczny frontend webowy działający w ramach SharePoint.

---

# 7. Własne akcje na dokumentach

Przykład:

Użytkownik zaznacza kilka dokumentów w bibliotece i wybiera:

```text
Wyślij do archiwum ERP
```

Architektura:

```text
Selected Documents
       |
       v
SPFx Command Set
       |
       v
API / Power Automate
       |
       v
Status / Notification
```

W takim scenariuszu SPFx ListView Command Set jest zwykle naturalniejszy niż budowanie osobnej aplikacji Canvas tylko po to, aby wykonać akcję na istniejącej bibliotece.

---

# 8. Niestandardowe renderowanie pól

Dla prostych zmian prezentacji często wystarczy SharePoint Column Formatting.

Przykład:

```text
Integrated          ✓
In Approval         ⧗
Rejected            ✕
Integration Error   ⚠
```

Jeżeli jednak potrzebne są:

- bardziej zaawansowana logika,
- dynamiczne zachowanie,
- integracja z API,
- dodatkowe akcje,

można rozważyć SPFx Field Customizer.

---

# 9. SPFx Extensions

SPFx obejmuje nie tylko webparty.

Dostępne są m.in.:

```text
Application Customizer
Field Customizer
ListView Command Set
Form Customizer
```

Pozwala to rozszerzać:

- strony,
- listy,
- biblioteki,
- formularze,
- toolbar,
- rendering pól.

---

# 10. Integracja z Microsoft 365

SPFx działa w kontekście użytkownika SharePoint i może integrować się z:

- SharePoint REST,
- Microsoft Graph,
- własnymi API,
- usługami Microsoft 365.

Komponent może korzystać z informacji o:

- użytkowniku,
- witrynie,
- stronie,
- tenantcie,
- aktualnym kontekście SharePoint.

---

# 11. SharePoint i Teams

W wybranych scenariuszach komponent SPFx może być wykorzystywany także w Microsoft Teams.

Możliwy model:

```text
            SPFx Component
             /          \
            /            \
    SharePoint          Teams
```

Daje to możliwość ponownego wykorzystania części UI w różnych powierzchniach Microsoft 365.

---

# 12. Koszt użycia SPFx

SPFx oznacza klasyczny lifecycle developerski.

```text
TypeScript
React
npm
build
test
bundle
package
.sppkg
App Catalog
deployment
versioning
maintenance
```

W porównaniu z Power Apps rośnie:

- ilość kodu,
- liczba zależności,
- odpowiedzialność za bezpieczeństwo,
- koszt testów,
- koszt deploymentu,
- koszt utrzymania.

Większa kontrola oznacza większą odpowiedzialność.

---

# 13. Bezpieczeństwo

Kod SPFx działa w kontekście SharePoint i bieżącego użytkownika.

Należy kontrolować:

- źródło kodu,
- zależności npm,
- aktualizacje bibliotek,
- uprawnienia do Microsoft Graph i innych API,
- App Catalog,
- proces publikacji,
- politykę wersjonowania.

Sekrety nie powinny być umieszczane bezpośrednio w kodzie klienta.

---

# 14. Kiedy nie stosować SPFx

SPFx nie jest dobrym wyborem, gdy wymaganie można prosto zrealizować standardowymi mechanizmami platformy.

Przykłady:

```text
prosty formularz
standardowy CRUD
przycisk Save
prosty workflow
standardowa lista danych
standardowy dashboard
```

Jeżeli rozwiązanie można sensownie zbudować przy użyciu:

```text
SharePoint
+
Power Apps
+
Power Automate
```

własny komponent SPFx może jedynie zwiększyć koszt utrzymania.

---

# 15. Kiedy zamiast SPFx wybrać własną aplikację webową

SPFx nie powinien być automatycznie wybierany tylko dlatego, że aplikacja ma działać w środowisku Microsoft 365.

Jeżeli rozwiązanie wymaga:

- wielu niezależnych modułów,
- własnego routingu,
- bardzo złożonego UX,
- dużej ilości logiki backendowej,
- własnego API,
- użytkowników spoza Microsoft 365,
- wielu źródeł danych,
- niezależnego lifecycle aplikacji,

warto rozważyć klasyczną aplikację webową.

Przykład:

```text
React / Angular / Blazor
          |
          v
         API
          |
          v
Dataverse / SQL / Services
```

SharePoint może wtedy pozostać jednym z systemów integracyjnych zamiast hostem całej aplikacji.

---

# 16. Drzewo decyzyjne

```text
Potrzebuję rozwiązania
        |
        v
Czy głównym miejscem pracy jest SharePoint?
        |
   +----+----+
   |         |
  NIE       TAK
   |         |
   |         v
   |   Czy standardowe webparty wystarczą?
   |         |
   |     +---+---+
   |     |       |
   |    TAK     NIE
   |     |       |
   |     |       v
   |     |   Czy potrzebuję głównie formularza
   |     |   lub aplikacji biznesowej?
   |     |       |
   |     |   +---+---+
   |     |   |       |
   |     |  TAK     NIE
   |     |   |       |
   |     | Power Apps  SPFx
   |     |
   |  standardowy SharePoint
   |
Power Apps / custom app
```

---

# 17. Macierz wyboru

| Potrzeba | Preferowany kierunek |
|---|---|
| prosty formularz | Power Apps |
| klasyczny CRUD | Power Apps |
| approval / workflow | Power Automate |
| aplikacja mobilna | Power Apps |
| prosty dashboard | standardowy SharePoint / Power BI |
| custom dashboard w portalu | SPFx |
| własna akcja w bibliotece | SPFx Command Set |
| zaawansowany custom rendering | SPFx |
| custom toolbar | SPFx |
| komponent zależny od kontekstu witryny | SPFx |
| duża niezależna aplikacja | custom web app |
| ciężka logika backendowa | API / kod backendowy |

---

# 18. Power Apps vs SPFx

## Power Apps

Zalety:

- szybkie tworzenie,
- low-code,
- formularze,
- Power Fx,
- integracja z konektorami,
- szybki prototyping.

Ograniczenia:

- mniejsza kontrola nad frontendem niż w klasycznym web development,
- specyficzny model UI,
- delegacja,
- ograniczenia przy bardzo niestandardowym UX.

## SPFx

Zalety:

- pełna kontrola nad frontendem,
- React / TypeScript,
- naturalna integracja z SharePoint,
- dostęp do kontekstu użytkownika i witryny,
- możliwość tworzenia extensions.

Koszt:

- więcej kodu,
- deployment,
- dependency management,
- testowanie,
- governance,
- utrzymanie.

---

# 19. SPFx nie usuwa ograniczeń SharePoint

SPFx zmienia sposób budowania frontendów.

Nie zmienia fundamentalnych ograniczeń SharePoint jako backendu.

Jeżeli źródło danych ma problemy z:

- List View Threshold,
- lookupami,
- security scopes,
- throttlingiem,
- modelem relacji,
- strukturą danych,

przeniesienie UI z Power Apps do SPFx nie usuwa tych problemów.

Przykład:

```text
Canvas App
      |
      v
SharePoint list 500 000 rekordów
      |
      v
problem modelu danych
```

Zmiana na:

```text
SPFx
 |
 v
ta sama lista
```

może pozostawić problem bez zmian.

Najpierw należy ustalić, czy problem leży w UI, czy w backendzie.

---

# 20. Architektura hybrydowa

SPFx może dobrze współpracować z innymi usługami.

Przykład:

```text
SharePoint Portal
      |
      v
SPFx Dashboard
      |
      +------> Dataverse
      |
      +------> API
      |
      +------> SharePoint Documents
```

W takim modelu:

- SharePoint pełni rolę portalu,
- Dataverse przechowuje dane domenowe,
- biblioteka SharePoint przechowuje dokumenty,
- SPFx odpowiada za portalowy UX.

---

# 21. Przykład architektury VCM

Rozszerzona architektura Vendor Contract Management może wyglądać tak:

```text
SharePoint Portal
      |
      v
SPFx Contract Dashboard
      |
      v
Dataverse
      |
      v
Power Automate
      |
      +--> Approval
      +--> API
      +--> Notification
      +--> Process Log
```

Dokumenty:

```text
SharePoint Document Library
```

Dane domenowe:

```text
Dataverse
```

Proces:

```text
Power Automate
```

UX portalowy:

```text
SPFx
```

Technologie mogą więc pełnić różne role w jednym rozwiązaniu.

---

# 22. Pytania przed wyborem SPFx

Przed podjęciem decyzji warto odpowiedzieć na pytania:

1. Czy użytkownik pracuje głównie w SharePoint?
2. Czy standardowe webparty rzeczywiście nie wystarczają?
3. Czy Power Apps nie rozwiązuje problemu prościej?
4. Czy wymagany jest niestandardowy UX?
5. Czy wymaganie dotyczy listy, biblioteki lub strony SharePoint?
6. Czy potrzebne są własne komendy?
7. Czy rozwiązanie wymaga integracji z Microsoft Graph lub API?
8. Czy zespół potrafi utrzymywać TypeScript i React?
9. Kto będzie utrzymywał rozwiązanie w kolejnych latach?
10. Czy problem dotyczy UI, czy modelu danych?

---

# 23. Anti-patterny

## SPFx do kosmetycznych zmian

Pisanie własnego komponentu tylko po to, aby zmienić kilka elementów wyglądu zwiększa koszt utrzymania bez istotnej wartości architektonicznej.

## Jeden gigantyczny webpart

Budowanie całego dużego systemu biznesowego jako jednego komponentu SPFx prowadzi do trudnego w utrzymaniu monolitu frontendowego.

## SPFx jako obejście ograniczeń backendu

Jeżeli problem wynika z modelu danych SharePoint, zmiana technologii frontendowej nie usuwa przyczyny.

## Brak zarządzania dependencies

Nieaktualizowane zależności npm zwiększają ryzyko techniczne i bezpieczeństwa.

## Hard-code konfiguracji

Adresy API, identyfikatory środowisk i inne wartości konfiguracyjne nie powinny być zaszyte bezpośrednio w kodzie.

## Sekrety w kodzie klienta

Sekrety nie powinny być przechowywane w bundle JavaScript ani innych zasobach dostępnych po stronie klienta.

---

# 24. Główny trade-off

```text
Power Apps
   |
   +--> szybszy development
   +--> mniej kodu
   +--> niższy koszt wejścia
   +--> mniejsza kontrola nad frontendem

SPFx
   |
   +--> pełniejsza kontrola
   +--> większa elastyczność UI
   +--> więcej kodu
   +--> większy koszt utrzymania
```

Żadna z technologii nie jest lepsza w każdym scenariuszu.

Wybór powinien wynikać z wymagań rozwiązania.

---

# 25. Podsumowanie

SPFx ma największy sens wtedy, gdy SharePoint pozostaje miejscem pracy użytkownika, ale standardowy interfejs platformy nie wystarcza.

Najprostszy model decyzyjny:

```text
standardowa funkcja SharePoint
        -> standardowy SharePoint

aplikacja biznesowa
        -> Power Apps

workflow
        -> Power Automate

rozszerzenie UX SharePoint
        -> SPFx

duża niezależna aplikacja
        -> custom web app
```

Najważniejsze rozróżnienie:

> **Power Apps buduje aplikację. SPFx rozszerza SharePoint.**

Jednocześnie:

> **SPFx daje większą kontrolę nad UI, ale nie usuwa ograniczeń SharePoint jako backendu.**

Jeżeli problemem jest model danych, zmiana frontendu nie rozwiązuje problemu.
