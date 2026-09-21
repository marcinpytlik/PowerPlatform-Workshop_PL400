# Power Platform – notatki architektoniczne

## Cel dokumentu

Dokument porządkuje najważniejsze zagadnienia architektoniczne związane z Power Apps, Power Automate, SharePoint, Dataverse, integracjami, obsługą błędów, obserwowalnością i ALM.

Materiał powstał jako rozwinięcie typowych pytań pojawiających się podczas projektowania rozwiązań Power Platform. Zamiast formatu FAQ został zapisany jako notatka techniczna.

---

# 1. Dobór technologii

## SharePoint vs Dataverse

SharePoint jest dobrym źródłem danych dla prostszych aplikacji, lekkich workflow, rozwiązań dokumentowych i modeli o niewielkiej liczbie relacji.

Dataverse staje się naturalniejszym wyborem, gdy rośnie znaczenie:

- relacji pomiędzy encjami,
- granularnego security,
- audytu,
- spójnego modelu domenowego,
- wielu aplikacji korzystających z tych samych danych,
- złożonego state machine,
- integracji,
- ALM,
- DEV / TEST / PROD.

Nie należy przyjmować zasady, że każda aplikacja Power Apps powinna od początku używać Dataverse. Wybór zależy od złożoności rozwiązania i przewidywanej skali.

---

## Power Apps vs aplikacja customowa

Power Apps dobrze sprawdza się, gdy rozwiązanie opiera się na:

- formularzach,
- CRUD,
- workflow,
- integracji z Microsoft 365,
- szybkim dostarczaniu funkcjonalności biznesowej.

Aplikacja customowa daje większą kontrolę nad:

- UX,
- wydajnością,
- routingiem,
- backendem,
- testowaniem,
- nietypowymi integracjami.

Power Apps nie zastępuje klasycznego developmentu. Jest innym narzędziem, odpowiednim dla określonej klasy problemów.

---

## Power Automate vs Azure Function

Praktyczna heurystyka:

```text
orkiestracja procesu
        -> Power Automate

ciężkie obliczenia / transformacje
        -> kod / Azure Function
```

To nie jest reguła absolutna.

Przy wyborze należy uwzględnić:

- wolumen,
- wymagany czas wykonania,
- złożoność transformacji,
- observability,
- retry,
- utrzymanie,
- kompetencje zespołu.

---

## Power Automate vs Logic Apps

Power Automate jest mocno związany z Power Platform i procesami biznesowymi.

Logic Apps jest bardziej naturalny w architekturze Azure i integracjach systemowych.

Oba rozwiązania mają wspólne obszary zastosowania, ale wybór powinien wynikać z kontekstu architektury, governance i lifecycle rozwiązania.

---

## Canvas App vs Model-driven App

Canvas App daje dużą kontrolę nad UX i sposobem interakcji użytkownika.

Model-driven App wykorzystuje model Dataverse i zapewnia szybkie budowanie formularzy, widoków, nawigacji i relacji.

Typowy podział:

```text
użytkownik biznesowy
      -> Canvas App

administracja / operations
      -> Model-driven App
```

Obie aplikacje mogą korzystać z tego samego Dataverse.

---

# 2. Power Apps – formularze i stan

## SubmitForm vs Patch

`SubmitForm()` dobrze pasuje do klasycznego formularza create/edit.

`Patch()` jest naturalny, gdy potrzebna jest:

- częściowa aktualizacja,
- zapis bez standardowego formularza,
- niestandardowa logika zapisu,
- aktualizacja wielu źródeł lub rekordów.

Problemem nie jest używanie `Patch()`, tylko stosowanie go bez potrzeby tam, gdzie standardowy formularz byłby czytelniejszy.

---

## Zmienne globalne

`Set()` tworzy stan globalny dostępny w całej aplikacji.

Nie jest to anti-pattern sam w sobie, ale duża liczba globalnych zmiennych utrudnia ustalenie:

- kto je ustawił,
- kiedy zostały zmienione,
- które ekrany od nich zależą.

Im większy zakres stanu, tym większe sprzężenie aplikacji.

---

## UpdateContext

`UpdateContext()` jest odpowiednie dla stanu lokalnego ekranu.

Przykładowo:

```text
czy panel jest otwarty
aktywny tryb formularza
lokalny filtr
tymczasowy stan UI
```

Dane potrzebne w wielu ekranach nie powinny być sztucznie utrzymywane jako lokalny context variable.

---

## Kolekcje

Kolekcje są przydatne dla:

- małych lokalnych zestawów danych,
- konfiguracji,
- tymczasowego stanu,
- danych offline.

Nie powinny być używane jako automatyczne obejście problemów delegacji.

```powerfx
ClearCollect(colAll, BigList)
```

nie zmienia niedelegowalnego zapytania w delegowalne.

---

# 3. Delegacja

Delegacja oznacza wykonanie zapytania po stronie źródła danych.

Przy poprawnej delegacji:

```text
Power Apps
   |
   v
Data Source
   |
Filter / Sort / Search
   |
   v
wynik
```

Przy niedelegowalnym wyrażeniu Power Apps pobiera ograniczony zestaw danych i przetwarza go lokalnie.

To może prowadzić nie tylko do problemów wydajnościowych, ale również do niepełnych wyników.

---

## Limit 500 / 2000

Domyślny limit lokalnego przetwarzania niedelegowalnych danych wynosi 500 rekordów.

Można go zwiększyć maksymalnie do 2000.

Zwiększenie limitu nie rozwiązuje problemu delegacji.

---

## Delegation warning

Delegation warning może oznaczać:

```text
nie "aplikacja będzie trochę wolniejsza"

ale

"aplikacja może zwrócić niepełny wynik"
```

Dlatego ostrzeżeń delegacji nie należy ignorować.

---

## LookUp i delegacja

Delegowalność `LookUp()` zależy od:

- źródła danych,
- typu pola,
- operatora,
- całego wyrażenia.

Nie ma poprawnej reguły typu:

```text
LookUp zawsze deleguje
```

lub:

```text
LookUp nigdy nie deleguje
```

---

# 4. Problem N+1

Problem N+1 pojawia się, gdy dla każdego elementu listy lub galerii wykonywane jest dodatkowe zapytanie.

Przykład:

```text
Gallery = 100 rekordów

row 1 -> LookUp
row 2 -> LookUp
row 3 -> LookUp
...
row 100 -> LookUp
```

Powoduje to dużą liczbę wywołań źródła danych.

Rozwiązaniem jest zwykle:

- lepszy model danych,
- ograniczenie zapytań,
- pobieranie potrzebnych danych wcześniej,
- delegowanie operacji do źródła.

---

# 5. Screen as a Feature

Ekran powinien reprezentować konkretną funkcję użytkownika.

Duża liczba kontrolek i warunków:

```text
Visible
DisplayMode
OnSelect
```

na jednym ekranie może prowadzić do silnego sprzężenia i trudnej diagnostyki.

Lepiej projektować ekran wokół pojedynczego celu niż używać jednego ekranu jako kontenera dla całej aplikacji.

---

# 6. Navigation Parameter

Przekazywanie kontekstu pomiędzy ekranami jest czytelniejsze niż bezpośrednie odwoływanie się do kontrolek znajdujących się na innych ekranach.

Zamiast:

```text
ScreenB czyta GalleryA.Selected
```

lepiej jawnie przekazać rekord lub identyfikator podczas nawigacji.

Zmniejsza to zależności pomiędzy ekranami.

---

# 7. App.OnStart i lazy loading

Duży `App.OnStart` może znacząco wydłużyć uruchamianie aplikacji.

Przy starcie powinny być ładowane tylko dane rzeczywiście potrzebne od początku.

Pozostałe dane powinny być pobierane wtedy, gdy są potrzebne.

To jest podstawowa idea lazy loading.

---

# 8. Kiedy logika nie powinna być w Canvas App

Canvas App nie powinien być miejscem dla całej logiki procesu.

Szczególnie warto wyprowadzić poza UI:

- długie procesy,
- retry,
- integracje,
- wieloetapowe approval,
- procesy wykonywane bez obecności użytkownika,
- operacje wymagające backendowej kontroli.

Najczęściej UI powinno inicjować intencję, a właściwy proces powinien być realizowany poza aplikacją.

---

# 9. Power Automate – monolit vs podział odpowiedzialności

Jeden duży flow nie jest automatycznie błędem.

Problem pojawia się, gdy zawiera jednocześnie:

```text
approval
integrację
notyfikacje
logging
error handling
transformacje
```

i poszczególne części zmieniają się niezależnie.

Wtedy warto rozważyć rozdzielenie odpowiedzialności.

---

# 10. Orchestrator

Orchestrator odpowiada za sterowanie przebiegiem procesu.

Przykład:

```text
VCM - Contract Submitted
        |
        +--> Approval
        +--> API Integration
        +--> Notification
        +--> Error Handler
```

Orchestrator powinien znać kolejność i warunki przejścia procesu, ale nie musi implementować całej logiki każdego kroku.

---

# 11. Child Flow

Child Flow ma sens, gdy logika:

- ma własną odpowiedzialność,
- jest powtarzalna,
- może być testowana niezależnie,
- zmienia się niezależnie,
- jest używana przez więcej niż jeden proces.

Rozbijanie każdej krótkiej sekwencji na child flow zwiększa złożoność bez realnej korzyści.

---

# 12. Child Flow a microservice

Child Flow nie powinien być automatycznie nazywany microservice.

Jest mechanizmem modularizacji automatyzacji Power Automate, ale nie daje automatycznie wszystkich właściwości architektury mikroserwisowej.

---

# 13. Trigger loops

Trigger obserwujący zmianę rekordu może zostać uruchomiony ponownie przez update wykonany przez ten sam flow.

Przykład:

```text
When item modified
        |
        v
Update item
        |
        v
When item modified
```

Rozwiązania obejmują:

- Trigger Conditions,
- status guard,
- techniczne flagi,
- jednoznaczny state machine.

---

# 14. Trigger Conditions vs Condition

Condition jako pierwsza akcja oznacza, że flow już się uruchomił.

Trigger Condition pozwala odrzucić zdarzenie wcześniej.

Dlatego, jeśli warunek można wiarygodnie ocenić na triggerze, jest to zwykle lepsze miejsce dla podstawowego guardu.

---

# 15. Trigger Guard

Trigger Guard określa warunek, przy którym proces naprawdę może się rozpocząć.

Przykład:

```text
Status = Submitted
```

chroni przed uruchamianiem procesu przy każdej zmianie rekordu.

---

# 16. Correlation ID

Correlation ID identyfikuje cały proces biznesowy.

Przykład:

```text
Contract
   |
Orchestrator Run A
   |
Child Flow Run B
   |
API Call
   |
Retry Run C
```

Run IDs są różne.

Correlation ID pozostaje ten sam.

GUID jest wygodnym sposobem implementacji correlation ID, ale wzorzec nie wymaga konkretnego typu identyfikatora.

---

# 17. Run ID vs Correlation ID

Run ID identyfikuje pojedyncze wykonanie konkretnego flow.

Correlation ID identyfikuje logiczny proces przebiegający przez wiele komponentów.

Dlatego oba identyfikatory mają inne zastosowanie.

---

# 18. Approval i brak odpowiedzi

Brak odpowiedzi approvera jest wymaganiem procesowym, a nie wyłącznie problemem technicznym.

Możliwe strategie:

- oczekiwanie,
- timeout,
- reminder,
- escalation,
- delegation,
- manual review.

Właściwy wybór powinien wynikać z polityki biznesowej.

---

# 19. Integracje HTTP i klasy błędów

Kod HTTP nie powinien być interpretowany bez kontekstu kontraktu API.

Przykładowo:

```text
400 -> często problem danych / requestu
409 -> może oznaczać konflikt biznesowy
429 -> throttling
5xx -> problem po stronie usługi
```

Znaczenie konkretnego statusu powinno wynikać z dokumentacji API.

---

# 20. Retry classification

Nie każdy błąd powinien być automatycznie retryowany.

Typowy podział:

```text
429 / transient 5xx
        -> retry może mieć sens

400 / błąd walidacji
        -> retry bez zmiany danych zwykle nie pomaga

409 biznesowy
        -> retry zależy od kontraktu API
```

Retry powinien być świadomą decyzją.

---

# 21. Idempotency

Operacja idempotentna może być wykonana wielokrotnie bez dodatkowego efektu końcowego.

Przykład:

```text
Set Status = Approved
```

może być naturalnie idempotentny.

Natomiast:

```text
Create Invoice
```

może tworzyć kolejny rekord przy każdym wywołaniu.

---

# 22. POST i idempotency

POST nie musi być nieidempotentny.

API może stosować:

- idempotency key,
- business key,
- deduplikację,
- upsert.

Pozwala to bezpiecznie obsługiwać retry.

---

# 23. Correlation ID nie zastępuje idempotency

Correlation ID pomaga śledzić proces.

Nie gwarantuje automatycznie, że ponowione wywołanie nie utworzy duplikatu.

Mechanizm idempotency musi być zaimplementowany przez klienta i/lub API.

---

# 24. Timeout po poprawnym wykonaniu operacji

Klasyczny scenariusz:

```text
POST
 |
API tworzy rekord
 |
odpowiedź ginie
 |
Power Automate widzi timeout
 |
retry
 |
drugi rekord?
```

Dlatego operacje tworzące dane muszą być projektowane z uwzględnieniem niepewności wyniku.

---

# 25. Failure Isolation

Awaria jednego elementu procesu nie powinna automatycznie unieważniać poprawnych wcześniejszych kroków.

Przykład:

```text
Approval OK
API OK
Email FAIL
```

Brak wiadomości e-mail nie powinien zmieniać zatwierdzonej umowy na Rejected.

---

# 26. DLP

Data Loss Prevention Policies kontrolują sposób używania connectorów w Power Platform.

Mogą ograniczać:

- które connectory są dozwolone,
- które mogą być używane razem,
- użycie HTTP,
- custom connectors,
- połączenia pomiędzy klasami danych.

Problemy z działaniem aplikacji lub flow mogą więc wynikać z governance tenantu, a nie z samego projektu rozwiązania.

---

# 27. Dataverse – model danych

Dataverse należy traktować jako platformę danych, a nie po prostu jako "SQL pod Power Apps".

Daje m.in.:

- tabele,
- relacje,
- security,
- auditing,
- Choices,
- alternate keys,
- solution-aware components.

---

# 28. Choice vs tekst

Choice ogranicza zbiór wartości do jawnie zdefiniowanych stanów.

Tekst pozwala na powstawanie wariantów typu:

```text
Approved
approved
APPROVED
Approve
```

Choice zwiększa spójność modelu.

---

# 29. Approval jako osobna tabela

Approval jest osobnym bytem, jeśli chcemy przechowywać historię wielu decyzji.

Przykład:

```text
Contract
   |
   +--> Legal Approval
   +--> Finance Approval
   +--> Management Approval
```

Pojedyncze pola na Contract szybko przestają wystarczać.

---

# 30. Alternate Key

GUID identyfikuje rekord technicznie.

Alternate Key reprezentuje unikalność biznesową.

Przykład:

```text
SupplierCode
ContractNumber
```

Alternate keys są szczególnie przydatne przy integracji i operacjach typu upsert.

---

# 31. Auditing vs Process Log

Auditing odpowiada głównie na pytanie:

```text
kto, kiedy i co zmienił?
```

Process Log odpowiada na pytanie:

```text
co zrobił proces?
```

To dwa różne mechanizmy i różne potrzeby.

---

# 32. Security Roles

Uprawnienia powinny wynikać z roli biznesowej.

Przykładowe role:

```text
Employee
Approver
Administrator
```

Przyznawanie pełnego dostępu wszystkim użytkownikom upraszcza development, ale nie jest poprawnym modelem bezpieczeństwa.

---

# 33. Source of Truth

Dla każdego typu informacji należy określić jedno miejsce będące źródłem prawdy.

Przykład VCM:

```text
Contract State
    -> Contract

Approval History
    -> Approval

Technical Events
    -> Process Log

Configuration
    -> Environment Variables
```

Powielanie tego samego stanu w wielu miejscach zwiększa ryzyko niespójności.

---

# 34. State Machine

Stan procesu powinien być jawnie zaprojektowany.

Przykład:

```text
Draft
  |
Submitted
  |
In Approval
  |------> Rejected
  |
Approved
  |
Integration Pending
  |------> Integration Error
  |
Integrated
```

Każdy stan powinien mieć określone poprawne przejścia.

---

# 35. Status biznesowy vs techniczny

`Approved` i `Integrated` nie oznaczają tego samego.

Approval opisuje decyzję biznesową.

Integration opisuje wynik technicznej komunikacji z systemem zewnętrznym.

Łączenie obu pojęć w jeden nieprecyzyjny status utrudnia diagnostykę i recovery.

---

# 36. Strangler Migration

Strangler Migration polega na stopniowym zastępowaniu starego systemu nowym.

```text
stary system działa
        |
budujemy nowy element
        |
przepinamy fragment
        |
test regresyjny
        |
kolejny fragment
        |
wyłączamy stary komponent
```

Zmniejsza zakres jednorazowej zmiany i ryzyko Big Bang Migration.

Nie każdy system pozwala jednak na łatwe rozdzielenie komponentów.

---

# 37. Model-driven App jako warstwa administracyjna

Model-driven App dobrze sprawdza się jako interfejs dla użytkowników administracyjnych i operacyjnych.

Przykład:

```text
Canvas
   -> pracownik

Model-driven
   -> administrator / operations

Dataverse
   -> wspólne dane
```

Nie trzeba budować w Canvas osobnych ekranów administracyjnych, jeśli standardowe możliwości Model-driven są wystarczające.

---

# 38. Configuration over Hard-code

Konfiguracja zależna od środowiska nie powinna być zaszyta bezpośrednio w aplikacji lub flow.

Przykłady:

```text
API Base URL
Support Email
Feature Flag
External System Identifier
```

Powinny być zarządzane jako konfiguracja.

---

# 39. Environment Variables

Environment Variables pozwalają przenosić Solution pomiędzy środowiskami bez zmiany logiki.

Przykład:

```text
DEV
VCM_API_BASE_URL = https://dev-api...

TEST
VCM_API_BASE_URL = https://test-api...
```

Zwykła Environment Variable nie powinna być traktowana jako magazyn sekretów.

---

# 40. Connection References

Connection Reference oddziela komponent Solution od konkretnego połączenia developera.

Solution może określić:

```text
potrzebuję połączenia Dataverse
```

bez trwałego związania go z:

```text
konkretnym connection z DEV
```

To jest istotny element ALM.

---

# 41. TRY / CATCH / FINALLY w Power Automate

W Power Automate wzorzec implementuje się najczęściej przy użyciu Scope i Configure run after.

```text
TRY
 |
CATCH
 |
FINALLY
 |
Terminate
```

Nie jest to konstrukcja języka programowania, ale odpowiada podobnej potrzebie architektonicznej.

---

# 42. FINALLY

FINALLY jest używany dla operacji, które powinny zostać wykonane niezależnie od sukcesu lub błędu.

Jeżeli `Terminate` zostanie wykonany wcześniej w CATCH, dalsza część procesu może nie zostać wykonana.

Dlatego kolejność ma znaczenie.

---

# 43. Business Error vs Technical Error

Przykłady biznesowych wyników:

```text
Approval Rejected
Limit przekroczony
Brak zgody biznesowej
```

Przykłady błędów technicznych:

```text
HTTP 500
timeout
brak connection
błąd connectora
```

Wynik biznesowy nie powinien automatycznie oznaczać Failed run.

---

# 44. Process Log

Process Log może przechowywać:

```text
Timestamp
Correlation ID
Run ID
Component
Action
Severity
Message
```

Jest szczególnie przydatny, gdy proces przechodzi przez wiele flowów i integracji.

---

# 45. Observability

Monitoring odpowiada na pytanie:

```text
czy coś jest nie tak?
```

Observability:

```text
dlaczego system zachował się w taki sposób?
```

Typowy zestaw identyfikatorów:

```text
Business ID
+ Correlation ID
+ Flow Run ID
+ Process Log
```

---

# 46. Run History

Run History jest bardzo dobrym źródłem diagnostyki konkretnego flow.

Nie zawsze wystarcza, gdy jeden proces obejmuje:

- kilka flowów,
- Canvas App,
- Dataverse,
- API,
- retry.

Dlatego potrzebna jest korelacja pomiędzy komponentami.

---

# 47. Live Monitor

Live Monitor pozwala analizować zachowanie Canvas App na poziomie technicznym.

Może pomóc zidentyfikować:

- wywołania connectorów,
- czas trwania operacji,
- błędy,
- Trace,
- kosztowne akcje.

Analiza powinna koncentrować się na konkretnych operacjach, a nie tylko na subiektywnym stwierdzeniu, że "aplikacja jest wolna".

---

# 48. Apply to each

`Apply to each` nie jest błędem samym w sobie.

Problem pojawia się, gdy wcześniej pobierany jest duży zbiór danych, z którego potrzebna jest niewielka część.

Przykład:

```text
Get 50 000
↓
Apply to each
↓
potrzebujemy 10
```

Lepszym rozwiązaniem jest filtracja przy źródle.

---

# 49. Concurrency

Równoległość może przyspieszyć niezależne operacje, ale może też powodować:

- większe obciążenie connectora,
- throttling,
- race conditions,
- konkurencyjne aktualizacje tego samego rekordu.

Concurrency powinno być świadomie projektowane.

---

# 50. Solutions i ALM

Solution jest jednostką przenoszenia i lifecycle komponentów Power Platform.

Typowy model:

```text
DEV
unmanaged
   |
export
   |
TEST
managed
   |
PROD
managed
```

DEV służy do developmentu.

Środowiska docelowe powinny otrzymywać kontrolowany artefakt.

---

# 51. Managed Solution

Managed Solution nie należy upraszczać do pojęcia "read-only".

To model zarządzania komponentami, ich zależnościami i lifecycle w środowisku docelowym.

---

# 52. Jedno Solution vs wiele Solutions

Dla małego i średniego rozwiązania jedno Solution często upraszcza lifecycle.

W większych systemach można rozdzielać Solutions według:

- domen,
- warstw,
- zespołów,
- niezależnych cykli wdrożeniowych.

Podział powinien wynikać z architektury, a nie z arbitralnej liczby komponentów.

---

# 53. Deployment DEV -> TEST

Typowa sekwencja:

```text
DEV
 |
Solution
 |
managed export
 |
TEST
 |
Connection References
 |
Environment Variables
 |
Security
 |
Smoke Test
 |
E2E
```

Po imporcie należy najpierw wykonać smoke test, a dopiero potem pełny test procesu.

---

# 54. Smoke Test

Smoke test powinien potwierdzić, że podstawowa instalacja działa.

Przykład:

```text
Solution istnieje
Model-driven App otwiera się
Contract można utworzyć
Connection References są poprawne
Environment Variables wskazują TEST
```

Dopiero po tym warto uruchamiać pełny proces biznesowy.

---

# 55. Low-code i dług techniczny

Low-code zmniejsza koszt budowy pierwszej wersji rozwiązania.

Nie usuwa problemów architektonicznych.

Przy braku kontroli można szybko stworzyć:

```text
wiele flowów
wiele zależności
dużo globalnego stanu
hard-code
duplikację logiki
brak obserwowalności
```

Łatwość tworzenia komponentów zwiększa potrzebę świadomego projektowania.

---

# 56. Modularność ma koszt

Zbyt mały podział prowadzi do monolitu.

Zbyt duży podział może prowadzić do:

```text
distributed spaghetti
```

Każde wydzielenie komponentu powinno mieć uzasadnienie:

- osobna odpowiedzialność,
- niezależny lifecycle,
- reuse,
- lepsza testowalność,
- ograniczenie sprzężenia.

---

# 57. Process Log i retencja

Process Log może szybko rosnąć.

Dlatego trzeba określić:

- okres retencji,
- zakres przechowywanych danych,
- sposób archiwizacji,
- mechanizm cleanup,
- wymagania audytowe.

Nie każdy techniczny szczegół musi być przechowywany bezterminowo.

---

# 58. Dane osobowe w logach

Do logów nie należy bez potrzeby kopiować:

- całych payloadów,
- danych osobowych,
- sekretów,
- tokenów,
- poufnych pól biznesowych.

Observability nie powinna zwiększać ryzyka bezpieczeństwa i compliance.

---

# 59. Secure Inputs / Outputs

Secure Inputs i Secure Outputs ograniczają widoczność danych w Run History.

Zwiększają ochronę danych, ale utrudniają diagnostykę.

Ich użycie powinno wynikać z charakteru danych i wymagań bezpieczeństwa.

---

# 60. Kryteria analizy architektonicznej

Przy ocenie rozwiązania Power Platform warto zawsze przejść przez następujące pytania:

```text
DANE
- gdzie są przechowywane?
- co jest source of truth?

STAN
- kto jest właścicielem zmiany?

PROCES
- kto orkiestruje?

RETRY
- czy operacja jest bezpieczna przy ponowieniu?

BŁĄD
- biznesowy czy techniczny?

CONCURRENCY
- co przy równoległym wykonaniu?

OBSERVABILITY
- jak odtworzyć timeline?

SECURITY
- kto może wykonać operację?

SCALE
- co stanie się przy 10x większym wolumenie?

ALM
- jak rozwiązanie przejdzie DEV -> TEST -> PROD?
```

To zestaw pytań, który pozwala analizować rozwiązanie niezależnie od konkretnego interfejsu Power Platform.

---

# 61. Podsumowanie

Najważniejsze zasady:

1. Źródło danych powinno pasować do złożoności modelu.
2. UI nie powinno posiadać całej logiki procesu.
3. Delegacja jest problemem poprawności, nie tylko wydajności.
4. Proces powinien mieć jawny state machine.
5. Jeden proces powinien mieć correlation ID.
6. Retry wymaga klasyfikacji błędów i idempotency.
7. Wynik biznesowy i błąd techniczny to różne pojęcia.
8. Observability musi obejmować więcej niż Run History.
9. Konfiguracja środowiskowa nie powinna być hard-code.
10. ALM powinien być częścią architektury od początku.
11. Modularność ma koszt i powinna mieć uzasadnienie.
12. Low-code nie zwalnia z projektowania.
