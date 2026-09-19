# Agenda szkolenia – Power Platform Advanced Workshop

## Forma

- 3 dni x 7 godzin merytorycznych.
- Około 30% architektura i wyjaśnienia.
- Około 70% demo, laboratoria i samodzielna praca.
- Jedna aplikacja rozwijana przez całe szkolenie.

# Dzień 1 – od pomysłu do działającej aplikacji

## 09:00–09:30 – Wprowadzenie i architektura rozwiązania

- wymagania biznesowe Vendor Contract Management,
- podział odpowiedzialności: aplikacja / workflow / dane / integracja,
- Canvas App, Power Automate, SharePoint, Dataverse, Model-driven App,
- architektura początkowa i docelowa.

## 09:30–10:30 – Projekt danych w SharePoint

- Suppliers,
- Contracts,
- ContractApprovals,
- dokumenty i załączniki,
- relacje realizowane przez lookup,
- indeksy i widoki,
- ograniczenia SharePoint jako bazy aplikacyjnej.

## 10:45–12:15 – Canvas App od zera

- ekran listy umów,
- formularz nowej umowy,
- walidacja,
- Patch vs SubmitForm,
- filtrowanie i wyszukiwanie,
- podstawy delegacji,
- obsługa stanów aplikacji.

## 12:45–14:15 – Pierwszy workflow Power Automate

- trigger po utworzeniu umowy,
- pobieranie danych,
- warunki biznesowe,
- approval,
- aktualizacja statusu,
- powiadomienie,
- Run after.

## 14:30–15:30 – HTTP/API i obsługa odpowiedzi

- HTTP request,
- Parse JSON,
- statusy 2xx/4xx/5xx,
- retry,
- timeout,
- 429 Too Many Requests,
- correlation ID.

## 15:30–16:00 – Retrospekcja architektoniczna

- co już działa,
- co zaczyna boleć,
- gdzie SharePoint przestaje być wygodny,
- przygotowanie migracji do Dataverse.

# Dzień 2 – Dataverse, Model-driven i utrzymywalna architektura

## 09:00–10:30 – Dataverse od podstaw

- tables i columns,
- choices,
- lookups,
- relacje 1:N i N:N,
- ownership,
- alternate keys,
- auditing,
- podstawy security roles,
- model Supplier–Contract–Approval–ProcessLog.

## 10:45–12:00 – Migracja rozwiązania SharePoint -> Dataverse

- migracja danych testowych,
- zmiana źródła danych Canvas App,
- refaktoryzacja Power Fx,
- zamiana triggera SharePoint na Dataverse,
- Update item -> Update a row,
- relacje zamiast ręcznego łączenia danych,
- test regresyjny SharePoint vs Dataverse.

## 12:30–13:30 – Model-driven App

- czym różni się od Canvas App,
- forms,
- views,
- navigation,
- related records,
- aplikacja administracyjna Contract Administration.

## 13:30–14:15 – Wielojęzyczność Canvas App

- Language(),
- tabela tłumaczeń,
- klucze zasobów,
- PL / EN / DE,
- unikanie tekstów wpisanych bezpośrednio w kontrolki.

## 14:30–15:30 – Refaktoryzacja Power Automate

- docelowy orchestrator,
- child flows / solution-aware flows,
- małe flowy o pojedynczej odpowiedzialności,
- przygotowanie do connection references,
- przygotowanie do environment variables,
- konfiguracja zamiast hard-code.

## 15:30–16:00 – Architektura: flow czy kod?

- Power Automate,
- Logic Apps,
- Azure Functions,
- API,
- podział odpowiedzialności między komponenty.

# Dzień 3 – jakość, diagnostyka, wydajność i deployment

## 09:00–10:15 – Error handling w Power Automate

- Scope TRY/CATCH/FINALLY,
- Configure run after,
- terminate,
- retry policy,
- timeout,
- logowanie błędów,
- ProcessLog.

## 10:15–11:15 – Diagnostyka "flow zrobił coś dziwnego"

- run history,
- inputs i outputs,
- trigger conditions,
- duplicate trigger,
- pętle wywołań,
- concurrency,
- race condition,
- ponowienia,
- correlation ID.

## 11:30–12:30 – Power Apps Monitor i testowanie

- Monitor w czasie rzeczywistym,
- Trace(),
- sieć i konektory,
- błędy Power Fx,
- testowanie Canvas App,
- scenariusze regresyjne.

## 13:00–14:00 – Performance i limity

- delegacja,
- filtrowanie u źródła,
- Get items,
- Filter Query,
- Select columns,
- pagination,
- SharePoint List Threshold,
- indeksowanie,
- throttling,
- ograniczanie Apply to each,
- unikanie N+1.

## 14:00–15:00 – Solutions i ALM

- solution components,
- publisher i prefix,
- unmanaged vs managed,
- dependencies,
- connection references,
- environment variables,
- solution layers,
- wersjonowanie.

## 15:00–15:45 – DEV → TEST → PROD

- eksport i import,
- managed solution,
- konfiguracja środowiskowa,
- deployment checklist,
- smoke test,
- rollback i upgrade strategy.

## 15:45–16:00 – Podsumowanie

- architektura rozwiązania końcowego,
- checklista projektowa,
- najważniejsze reguły produkcyjne.
