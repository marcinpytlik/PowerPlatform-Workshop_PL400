# Kiedy stosować własny webpart w SharePoint Online

## Cel materiału

Ten dokument pomaga podjąć decyzję, kiedy wystarczy standardowy SharePoint, kiedy lepszym wyborem jest Power Apps, a kiedy warto napisać własny komponent w SharePoint Framework (SPFx).

> **Power Apps służy przede wszystkim do budowania aplikacji. SPFx służy przede wszystkim do rozszerzania doświadczenia SharePoint.**

## 1. Czym jest własny webpart

W nowoczesnym SharePoint Online rekomendowanym modelem rozszerzania interfejsu jest SharePoint Framework (SPFx). SPFx pozwala budować własne komponenty klienckie, najczęściej w TypeScript/React/JavaScript, pakowane jako `.sppkg` i wdrażane przez App Catalog.

Dokumentacja:
- https://learn.microsoft.com/en-us/sharepoint/dev/spfx/sharepoint-framework-overview
- https://learn.microsoft.com/en-us/sharepoint/dev/spfx/web-parts/overview-client-side-web-parts
- https://learn.microsoft.com/en-us/sharepoint/dev/spfx/extensions/overview-extensions

## 2. Kiedy SPFx ma sens

SPFx ma sens przede wszystkim wtedy, gdy głównym miejscem pracy użytkownika jest SharePoint, ale standardowe webparty i Power Apps nie dają odpowiedniego UX lub poziomu integracji.

Typowe przypadki:
- niestandardowy dashboard osadzony na stronie SharePoint,
- specjalna tabela lub grid,
- drag & drop,
- własny komponent React,
- akcje na zaznaczonych dokumentach,
- niestandardowe renderowanie pól,
- rozszerzenie toolbaru,
- integracja mocno związana z kontekstem bieżącej witryny.

## 3. Najważniejsze pytanie

> Czy buduję aplikację, czy rozszerzam SharePoint?

Jeśli użytkownik ma pozostać na stronie SharePoint i potrzebuje tam niestandardowej wizualizacji, interakcji lub integracji z kontekstem witryny, SPFx jest naturalnym kandydatem.

## 4. Przykład: dashboard VCM

Przykładowy webpart:

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

Taki komponent może pobierać dane z SharePoint, Dataverse lub API i prezentować je bezpośrednio w portalu SharePoint.

## 5. Kiedy Power Apps jest lepsze

Power Apps preferujemy, gdy wymaganie wygląda jak klasyczna aplikacja biznesowa:
- formularz,
- CRUD,
- kilka ekranów,
- walidacja,
- proces użytkownika,
- workflow.

Przykład: New Contract, Edit Contract, Submit, Approve, View status.

W takim przypadku pisanie SPFx może tylko zwiększyć koszt implementacji i utrzymania.

## 6. Kiedy SPFx zaczyna wygrywać z Power Apps

Sygnały:
- bardzo niestandardowy UX,
- zaawansowany grid,
- drag & drop,
- własne menu lub akcje,
- wyspecjalizowane wizualizacje,
- integracja z kontekstem strony SharePoint.

Canvas App daje dużą elastyczność, ale nadal działa w modelu Power Apps. SPFx daje klasyczny frontend webowy uruchomiony w SharePoint.

## 7. Przykład: własna akcja na dokumentach

Użytkownik zaznacza kilka dokumentów i ma dostać komendę `Wyślij do archiwum ERP`.

```text
Selected documents
       |
       v
Custom command
       |
       v
API / Power Automate
       |
       v
Status / notification
```

W takim scenariuszu naturalnym rozwiązaniem jest SPFx ListView Command Set, a nie osobna Canvas App.

## 8. Przykład: własne renderowanie pola

Jeśli chcemy pokazać statusy z ikonami, tooltipami i bardziej złożonym zachowaniem, najpierw warto sprawdzić column formatting. Gdy potrzebna jest logika wykraczająca poza formatting, można rozważyć SPFx Field Customizer.

## 9. SPFx Extensions

SPFx to nie tylko webparty. Dostępne są m.in.:
- Application Customizer,
- Field Customizer,
- ListView Command Set,
- Form Customizer.

Dzięki temu możemy rozszerzać strony, listy, biblioteki, formularze, toolbar i rendering pól.

## 10. Integracja z Microsoft 365

SPFx działa w kontekście użytkownika SharePoint i może integrować się z SharePoint REST, Microsoft Graph oraz własnymi API. Pozwala wykorzystywać kontekst użytkownika, witryny i strony.

## 11. SharePoint i Teams

W odpowiednich scenariuszach komponent SPFx może być wykorzystany zarówno w SharePoint, jak i w Microsoft Teams.

## 12. Cena użycia SPFx

SPFx oznacza klasyczny lifecycle developerski:

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

> Większa kontrola oznacza większą odpowiedzialność.

## 13. Bezpieczeństwo

Kod SPFx działa w kontekście użytkownika i strony SharePoint. Trzeba kontrolować źródło kodu, zależności npm, uprawnienia do API, App Catalog, proces akceptacji i aktualizacje.

SPFx nie powinien być traktowany jako sposób na obchodzenie mechanizmów bezpieczeństwa SharePoint.

## 14. Kiedy NIE pisać własnego webparta

Nie pisz SPFx tylko po to, aby zmienić kilka szczegółów wyglądu albo gdy wymaganiem jest jedynie formularz, tabela, przycisk Save lub workflow, które można sensownie zrealizować standardowym SharePoint, Power Apps i Power Automate.

## 15. Kiedy zamiast SPFx zrobić własną aplikację

Jeśli wymagania obejmują dużą niezależną aplikację, wiele modułów, własny routing, złożony UX, dużo logiki backendowej, własne API albo użytkowników spoza Microsoft 365, warto zapytać, czy SharePoint w ogóle powinien być hostem tej aplikacji.

Możliwy model:

```text
React / Angular / Blazor
          |
          v
         API
          |
          v
Dataverse / SQL / services
```

## 16. Drzewo decyzyjne

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

## 17. Szybka macierz wyboru

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
| komponent mocno związany z kontekstem witryny | SPFx |
| duża niezależna aplikacja | custom web app |
| ciężka logika backendowa | API / kod backendowy |

## 18. SPFx nie usuwa ograniczeń SharePoint

To bardzo ważne:

> SPFx daje większą kontrolę nad frontendem, ale nie usuwa ograniczeń SharePoint jako backendu.

Jeśli lista ma problemy z List View Threshold, lookupami, security scopes, throttlingiem lub modelem relacji, napisanie webparta nie sprawi, że te ograniczenia znikną.

Przykład błędnego wniosku:

```text
Canvas App ma problem z listą 500 000 rekordów
i złożonym modelem relacji
        |
        v
napiszmy SPFx
```

Poprawne pytanie brzmi:

> Czy problemem jest UI, czy model danych?

Jeśli problemem jest model danych, SPFx na tej samej liście może nadal mieć te same problemy backendowe.

## 19. Dobry scenariusz hybrydowy

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

SharePoint może pełnić rolę portalu, Dataverse przechowywać dane domenowe, biblioteka SharePoint dokumenty, a SPFx składać wszystko w spójny UX.

## 20. VCM – możliwa architektura rozszerzona

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

Dokumenty mogą pozostać w SharePoint Document Library, dane domenowe w Dataverse, proces w Power Automate, a UX portalowy w SPFx.

## 21. Pytania przed wyborem SPFx

1. Czy użytkownik ma pracować bezpośrednio w SharePoint?
2. Czy standardowy webpart naprawdę nie wystarcza?
3. Czy Power Apps nie rozwiązuje problemu prościej?
4. Czy potrzebujemy custom UX?
5. Czy wymaganie dotyczy strony, biblioteki lub listy SharePoint?
6. Czy potrzebujemy własnych komend?
7. Czy potrzebujemy integracji z Microsoft Graph lub własnym API?
8. Czy zespół potrafi utrzymywać TypeScript / React?
9. Kto będzie utrzymywał rozwiązanie za dwa lata?
10. Czy problem leży w UI, czy w modelu danych?

## 22. Anti-patterny

- Pisanie SPFx tylko dla drobnych zmian wyglądu.
- Budowanie całego systemu biznesowego jako jednego ogromnego webparta.
- Używanie SPFx jako obejścia ograniczeń modelu danych SharePoint.
- Brak procesu aktualizacji zależności npm.
- Hard-code endpointów i konfiguracji środowiskowej.
- Umieszczanie sekretów w kodzie klienta.

## 23. Najważniejszy trade-off

```text
Power Apps
   |
   +--> szybkość developmentu
   +--> mniej kodu
   +--> mniej kontroli

SPFx
   |
   +--> więcej kodu
   +--> większy koszt
   +--> większa kontrola
```

Nie istnieje technologia lepsza w każdym przypadku. Istnieje technologia lepiej dopasowana do problemu.

## 24. Jak powiedzieć to uczestnikom

> Jeśli potrzebuję aplikacji biznesowej, najpierw patrzę na Power Apps.

> Jeśli potrzebuję rozszerzyć istniejące doświadczenie SharePoint, patrzę na SPFx.

> Jeśli buduję dużą niezależną aplikację, pytam, czy SharePoint w ogóle powinien być jej hostem.

## 25. Najważniejsze zdania na slajd

> **Power Apps buduje aplikację. SPFx rozszerza SharePoint.**

> **SPFx daje większą kontrolę nad UI, ale nie usuwa ograniczeń SharePoint jako backendu.**

> **Jeśli problemem jest model danych, zmiana frontendu nie rozwiązuje problemu.**

## 26. Połączenie z LAB 01 i LAB 05

Po LAB 01:

> Na tym etapie aplikacja jest prosta. Power Apps i SharePoint dobrze pasują do problemu.

Następnie:

> Gdyby wymaganiem był niestandardowy dashboard osadzony bezpośrednio w portalu SharePoint, moglibyśmy rozważyć SPFx.

Przed LAB 05:

> Nasz problem nie polega jednak na braku customowego UI. Problemem zaczyna być model danych, relacje, stan procesu i ALM. Dlatego nie rozwiązujemy go SPFx-em. Migrujemy model danych do Dataverse.

To pokazuje różnicę pomiędzy problemem UI a problemem architektury danych.