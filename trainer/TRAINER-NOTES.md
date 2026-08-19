# Notatki dla prowadzącego

## Zasada prowadzenia

Nie pokazuj funkcji jako oderwanych elementów. Każdy nowy mechanizm powinien wynikać z problemu, który pojawił się w rozwijanej aplikacji.

## Moment 1 – SharePoint

Pozwól uczestnikom zauważyć, że rozwiązanie działa, ale model danych i proces stają się coraz trudniejsze do utrzymania.

## Moment 2 – Dataverse

Nie przedstawiaj Dataverse jako "lepszego SharePointa". Pokaż relacje, security, auditing i model danych.

## Moment 3 – jeden duży flow

Najpierw zbuduj prostszy monolit, potem przeprowadź refaktoryzację. Dzięki temu uczestnicy widzą powód istnienia child flows i podziału odpowiedzialności.

## Moment 4 – awaria

Celowo wywołaj:

- 500,
- 429,
- ponowne wyzwolenie flow przez Update,
- dwa równoległe uruchomienia.

Nie pokazuj od razu rozwiązania. Najpierw diagnoza.

## Moment 5 – ALM

Solutions pojawiają się dopiero wtedy, gdy uczestnicy mają już realne komponenty do przeniesienia między środowiskami.
