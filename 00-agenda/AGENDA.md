# Agenda szkolenia – Power Platform Advanced Workshop

## Forma

- 3 dni × 7 godzin zegarowych (09:00–16:00 z przerwami).
- Około 30% architektura i wyjaśnienia.
- Około 70% demo, laboratoria i samodzielna praca.
- Jedna aplikacja rozwijana przez całe szkolenie.

To nie jest kurs egzaminacyjny. Nazwa PL-400 w repozytorium jest robocza.

Czas poniżej jest zgrany z realnym tempem sali. LAB 08 jest opcjonalny. LAB 11 i LAB 13 idą w wariancie skróconym. Pełne wersje tych labów zostają w repozytorium jako materiał własny albo dzień 4.

# Dzień 1 – od pomysłu do działającej aplikacji

## 09:00–09:25 – Wprowadzenie i architektura rozwiązania

- wymagania biznesowe Vendor Contract Management,
- podział odpowiedzialności: aplikacja / workflow / dane / integracja,
- Canvas App, Power Automate, SharePoint jako prototyp,
- architektura początkowa. Docelową Dataverse zostawiamy na dzień 2.

## 09:25–10:35 – Projekt danych w SharePoint (LAB 01)

- Suppliers, Contracts, ContractApprovals,
- dokumenty i załączniki – tylko omówienie,
- relacje realizowane przez lookup,
- indeksy i widoki,
- ograniczenia SharePoint jako bazy aplikacyjnej.

## 10:50–12:20 – Canvas App od zera (LAB 02)

- ekran listy umów,
- formularz nowej umowy,
- walidacja i `SubmitForm`,
- filtrowanie i wyszukiwanie,
- podstawy delegacji – zapisujemy ostrzeżenie, nie omijamy go kolekcją,
- `Notify()` i `Trace()`.

## 12:50–14:20 – Pierwszy workflow Power Automate (LAB 03)

- trigger po utworzeniu lub zmianie umowy,
- warunek `Submitted`,
- correlation ID,
- approval zależny od kwoty,
- aktualizacja statusu,
- powiadomienie,
- pierwszy podgląd drugiego runu po `Update`.

## 14:35–15:50 – HTTP, Settings, Run after (LAB 04)

- kontrakt `supplierCode` + mock API,
- HTTP 201 i zapis `ExternalSystemId`,
- timeout, retry, Secure inputs/outputs,
- 409 vs 500,
- 429: retry None vs retry policy.

Pełna macierz testów B/timeout jest demo prowadzącego, jeśli czas się kończy.

## 15:50–16:00 – Retrospekcja architektoniczna

- co już działa,
- co zaczyna boleć,
- gdzie SharePoint przestaje być wygodny,
- przygotowanie migracji do Dataverse.

# Dzień 2 – Dataverse, Model-driven i utrzymywalna architektura

## 09:00–10:45 – Dataverse od podstaw (LAB 05)

- Publisher i jedno Solution `Vendor Contract Management`,
- tables i columns,
- choices,
- lookups i relacje 1:N (N:N tylko jako dyskusja – model VCM ich nie potrzebuje),
- ownership,
- alternate keys,
- auditing,
- podstawy security roles,
- model Supplier–Contract–Approval–ProcessLog.

Relacje N:N są tematem dyskusji, nie częścią modelu VCM.

## 11:00–12:30 – Migracja SharePoint -> Dataverse (LAB 06)

- migracja danych testowych,
- zmiana źródła danych Canvas App ekran po ekranie,
- refaktoryzacja Power Fx,
- zamiana triggera SharePoint na Dataverse,
- Update item -> Update a row,
- relacje zamiast ręcznego łączenia danych,
- test regresyjny SharePoint vs Dataverse,
- wyłączenie starego flow.

## 13:00–14:00 – Model-driven App (LAB 07)

- czym różni się od Canvas App,
- forms, views, navigation, related records,
- aplikacja administracyjna Contract Administration.

## 14:00–14:15 – Bufor albo LAB 08

Wielojęzyczność Canvas App jest **opcjonalna**. Robimy ją tylko wtedy, gdy LAB 07 skończył się przed 13:50 i migracja nie ma długów. W przeciwnym razie – praca własna.

- `Language()`, tabela tłumaczeń, klucze, PL / EN / DE,
- unikanie tekstów wpisanych bezpośrednio w kontrolki.

## 14:15–15:15 – Projekt refaktoryzacji Power Automate

- docelowy orchestrator i child flows,
- małe flowy o pojedynczej odpowiedzialności,
- przygotowanie do connection references i environment variables,
- konfiguracja zamiast hard-code.

Implementacja podziału jest w LAB 12. Tu rysujemy cięcia.

## 15:30–16:00 – Architektura: flow czy kod?

- Power Automate,
- Logic Apps,
- Azure Functions,
- API,
- podział odpowiedzialności między komponenty.
- ćwiczenie E06.

# Dzień 3 – jakość, diagnostyka, wydajność i deployment

## 09:00–10:15 – Error handling w Power Automate (LAB 09)

- Scope TRY/CATCH/FINALLY,
- Configure run after,
- `Terminate` dopiero po FINALLY,
- retry policy i timeout,
- logowanie błędów do ProcessLog.

## 10:15–11:15 – Diagnostyka incydentu (LAB 10)

- jeden przygotowany wariant prowadzącego,
- run history, inputs i outputs,
- trigger loop, retry, race, stale write,
- correlation ID,
- raport incydentu przed poprawką.

## 11:30–12:00 – Power Apps Monitor

- Monitor w czasie rzeczywistym,
- `Trace()`,
- sieć i konektory,
- błędy Power Fx.

## 12:00–12:30 – Performance – wariant skrócony (LAB 11)

- Get items bez filtra vs Filter Query,
- delegacja: brak błędu ≠ poprawny wynik,
- 429 i concurrency – omówienie, nie pełny pomiar na 5000 rekordach.

## 13:00–14:15 – Solutions i ALM (LAB 12)

- to samo Solution, wersja 1.0.0.0,
- unmanaged vs managed,
- connection references,
- environment variables,
- usunięcie hard-code,
- dependencies i Solution Checker jeśli dostępny.

## 14:15–15:15 – DEV → TEST – wariant skrócony (LAB 13)

- eksport managed,
- import, connection references, environment variables,
- smoke test u wszystkich,
- E2E i negative test jako demo prowadzącego,
- rollback / upgrade – omówienie.

## 15:15–15:45 – Ćwiczenia i pytania

- E02, E03, E06 albo E07,
- checklista projektowa.

## 15:45–16:00 – Podsumowanie

- architektura rozwiązania końcowego,
- trzy reguły produkcyjne: status biznesowy vs integracja, diagnoza przed fixem, zmiana w DEV.

# Dzień 4 – opcjonalny

Jeżeli jest dodatkowy dzień, wracamy do pełnych wersji:

- LAB 08 całość + słownik w Dataverse,
- LAB 11 z większym datasetem, indeksami i concurrency,
- LAB 13 E2E i negative test u każdego, Pipelines,
- implementacja child flows z LAB 12.
