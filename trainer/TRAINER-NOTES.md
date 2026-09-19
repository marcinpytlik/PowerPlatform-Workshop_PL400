# Notatki dla prowadzącego

## Forma

To jest **Power Platform Advanced Workshop**, nie kurs egzaminacyjny PL-400. Uczymy utrzymywalnego rozwiązania: jeden proces, od prototypu SharePoint do managed Solution.

Nazwa repozytorium z PL-400 jest robocza. Na sali mówene jest: Advanced Workshop / Vendor Contract Management.

## Zasada prowadzenia

Nie pokazywać funkcji jako oderwanych elementów. Każdy nowy mechanizm powinien wynikać z problemu, który pojawił się w rozwijanej aplikacji.

Skrypty dni:

- [Dzień 1](SCRIPT-DAY-1.md)
- [Dzień 2](SCRIPT-DAY-2.md)
- [Dzień 3](SCRIPT-DAY-3.md)

Awarie: [DEMO-FAILURES.md](DEMO-FAILURES.md).
Obejścia: [PLAN-B.md](PLAN-B.md).
Setup: [../SETUP.md](../SETUP.md).

## Moment 1 – SharePoint

Pozwól uczestnikom zauważyć, że rozwiązanie działa, ale model danych i proces stają się coraz trudniejsze do utrzymania.

## Moment 2 – Dataverse

Nie przedstawiać Dataverse jako „lepszego SharePointa”. Pokazać relacje, security, auditing i model danych.

Jedno Solution: `Vendor Contract Management`, prefix `vcm`. DEV jest środowiskiem, nie członem nazwy Solution.

## Moment 3 – jeden duży flow

Najpierw zbuduj prostszy monolit, potem przeprowadź refaktoryzację. Dzięki temu uczestnicy widzą powód istnienia child flows i podziału odpowiedzialności.

W dniu 2 rysujemy podział. W dniu 3 pakujemy go do Solution – implementacja child flows nie jest blockerem.

## Moment 4 – awaria

Celowo wywołaj jedną rzecz na raz:

- 500,
- 429,
- ponowne wyzwolenie flow przez Update,
- dwa równoległe uruchomienia.

Nie pokazywać od razu rozwiązania. Najpierw diagnoza.

## Moment 5 – ALM

Solutions pojawiają się dopiero wtedy, gdy uczestnicy mają już realne komponenty do przeniesienia między środowiskami. Nie twórz drugiego Solution przed deploymentem.

## Czas – co ciąć

Agenda jest zgrana z realnym 3×7 h. Gdy grupa wypada z rytmu:

| Priorytet | Zostaje | Wychodzi |
|---|---|---|
| Musi być | LAB 01–07, 09, 12, 13 smoke | pełna macierz HTTP, Pipelines |
| Warto | LAB 10 jeden wariant, LAB 11 Filter Query | 50 000 rekordów, wszystkie A–E |
| Opcja | LAB 08, child flows, E2E każdego | dzień 4 |

## Kontrakt API

Ciało requestu zawsze:

```text
contractNumber, supplierCode, amount, currency, correlationId
```

Nie wysyłamy nazwy dostawcy jako klucza biznesowego. Tryby mock API: numer umowy, nagłówek `x-mock-mode` albo `/admin/mode`.
