# Power Platform Advanced Workshop

Warsztat zaawansowany, nie kurs egzaminacyjny. Nazwa `PL400` w repozytorium jest robocza.

## Projekt szkoleniowy

**Vendor Contract Management** – aplikacja do obsługi umów z dostawcami, rozwijana od prostego rozwiązania Canvas App + SharePoint do rozwiązania opartego o Dataverse, Model-driven App, Power Automate, API oraz ALM.

Przed dniem 1 wykonaj [`SETUP.md`](SETUP.md). Mock API: [`mock-api/README.md`](mock-api/README.md). Skrypty sali: [`trainer/`](trainer/).

## Cel szkolenia

Uczestnik buduje jedną aplikację od zera i w kolejnych modułach poznaje:

- architekturę Power Platform,
- SharePoint jako źródło danych oraz jego ograniczenia,
- Canvas Apps,
- Power Automate,
- Dataverse,
- Model-driven Apps,
- aplikacje wielojęzyczne,
- error handling i monitoring,
- optymalizację wydajności,
- integrację HTTP/API,
- Solutions i ALM,
- deployment DEV -> TEST -> PROD.

## Scenariusz biznesowy

Proces obsługuje:

1. Rejestrację dostawcy.
2. Rejestrację umowy.
3. Wieloetapową akceptację.
4. Integrację z systemem zewnętrznym.
5. Rejestr błędów i zdarzeń procesu.
6. Administrację przez aplikację Model-driven.
7. Przenoszenie rozwiązania między środowiskami.

## Architektura docelowa

```text
Canvas App
    |
    v
Dataverse
    |
    v
Power Automate Orchestrator
    |
    +--> Approval Flow
    +--> API Integration Flow
    +--> Notification Flow
    +--> Process Log

Model-driven App
    |
    +--> administracja i obsługa procesu
```

## Struktura repozytorium

- `SETUP.md` – tenant, licencje, środowiska, DLP, konta, checklisty.
- `00-agenda` – agenda 3 dni zgranych z realnym czasem sali.
- `01-architecture` – wymagania i decyzje architektoniczne.
- `02-sharepoint` – model początkowy SharePoint.
- `03-canvas-app` – projekt aplikacji Canvas.
- `04-power-automate` – flowy i wzorce.
- `05-dataverse` – docelowy model danych.
- `06-model-driven` – aplikacja administracyjna.
- `07-multilanguage` – słownik UI; LAB 08 jest opcjonalny.
- `08-error-handling` – wzorce obsługi błędów.
- `09-monitoring` – troubleshooting i monitoring.
- `10-performance` – optymalizacja i limity.
- `11-api-integration` – kontrakt OpenAPI.
- `mock-api` – serwer 201 / 409 / 429 / 500 / timeout.
- `12-solutions-alm` – Solutions i wersjonowanie.
- `13-deployment` – DEV/TEST/PROD.
- `labs` – laboratoria prowadzone krok po kroku.
- `exercises` – zadania samodzielne.
- `solutions` – oczekiwane kierunki rozwiązań.
- `trainer` – skrypty dni, awarie, plan B.

## Konwencja nazewnicza

Prefix publishera: `vcm`. Jedno Solution: `Vendor Contract Management`. DEV/TEST to środowiska, nie człony nazwy Solution.

Tabele – nazwa wyświetlana i schema:

| Wyświetlana | Schema |
|---|---|
| Supplier | `vcm_Supplier` |
| Contract | `vcm_Contract` |
| Approval | `vcm_Approval` |
| Process Log | `vcm_ProcessLog` |

Flowy:

| Etap | Nazwa |
|---|---|
| Prototyp SharePoint (LAB 03–04) | `VCM - Contract Submitted - SP` |
| Orchestrator Dataverse (LAB 06) | `VCM - Contract Submitted` |
| Ta sama logika z TRY/CATCH (LAB 09) | `VCM - Contract Submitted - v2` |
| Docelowy podział (LAB 12) | `VCM - Contract Submitted` + `VCM - Approval` + `VCM - API Integration` + `VCM - Notification` + `VCM - Error Handler` |

Aplikacje: `VCM - Contract Portal` (Canvas), `VCM - Contract Administration` (Model-driven).

## Wersjonowanie

```text
MAJOR.MINOR.BUILD.REVISION
1.0.0.0
1.1.0.0
1.1.1.0
2.0.0.0
```

## Środowiska

- DEV – unmanaged.
- TEST – managed.
- PROD – managed.


## Rozbudowane laboratoria

Komplet instrukcji krok po kroku znajduje się w [`labs/README.md`](labs/README.md). Laboratoria LAB 01–13 prowadzą od modelu SharePoint, przez Canvas App i Power Automate na SharePoint, świadomą migrację do Dataverse, aż do managed Solution oraz deploymentu DEV -> TEST.

W agendzie 3-dniowej LAB 08 jest opcjonalny, a LAB 11 i LAB 13 idą w wariancie skróconym opisanym na początku tych plików.
