# Power Platform Advanced Workshop

## Projekt szkoleniowy

**Vendor Contract Management** – aplikacja do obsługi umów z dostawcami, rozwijana od prostego rozwiązania Canvas App + SharePoint do rozwiązania opartego o Dataverse, Model-driven App, Power Automate, API oraz ALM.

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
    +--> ProcessLog

Model-driven App
    |
    +--> administracja i obsługa procesu
```

## Struktura repozytorium

- `00-agenda` – agenda szkolenia.
- `01-architecture` – wymagania i decyzje architektoniczne.
- `02-sharepoint` – model początkowy SharePoint.
- `03-canvas-app` – projekt aplikacji Canvas.
- `04-power-automate` – flowy i wzorce.
- `05-dataverse` – docelowy model danych.
- `06-model-driven` – aplikacja administracyjna.
- `07-multilanguage` – wielojęzyczność.
- `08-error-handling` – wzorce obsługi błędów.
- `09-monitoring` – troubleshooting i monitoring.
- `10-performance` – optymalizacja i limity.
- `11-api-integration` – integracja HTTP/API.
- `12-solutions-alm` – Solutions i wersjonowanie.
- `13-deployment` – DEV/TEST/PROD.
- `labs` – laboratoria prowadzone krok po kroku.
- `exercises` – zadania samodzielne.
- `solutions` – oczekiwane rozwiązania i checklisty.
- `trainer` – notatki prowadzącego.

## Konwencja nazewnicza

Przykładowy prefix solution: `vcm`.

- `vcm_Supplier`
- `vcm_Contract`
- `vcm_Approval`
- `vcm_ProcessLog`
- `VCM - Contract Created`
- `VCM - Approval`
- `VCM - API Integration`

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

Komplet instrukcji krok po kroku znajduje się w [`labs/README.md`](labs/README.md). Laboratoria LAB 01–12 prowadzą od modelu SharePoint, przez Canvas App, Power Automate i Dataverse, aż do managed Solution oraz deploymentu DEV -> TEST.
