# Notatki dla prowadzącego

## Zasada prowadzenia

Nie pokazywać funkcji jako oderwanych elementów. Każdy nowy mechanizm powinien wynikać z problemu, który pojawił się w rozwijanej aplikacji.

## Moment 1 – SharePoint

Pozwolic uczestnikom zauważyć, że rozwiązanie działa, ale model danych i proces stają się coraz trudniejsze do utrzymania.

## Moment 2 – Dataverse

Nie przedstawiać Dataverse jako "lepszego SharePointa". Pokazać relacje, security, auditing i model danych.

## Moment 3 – jeden duży flow

Najpierw zbuduj prostszy monolit, potem przeprowadź refaktoryzację. Dzięki temu uczestnicy widzą powód istnienia child flows i podziału odpowiedzialności.

## Moment 4 – awaria

Celowo wywołaj:

- 500,
- 429,
- ponowne wyzwolenie flow przez Update,
- dwa równoległe uruchomienia.

Nie pokazywac od razu rozwiązania. Najpierw diagnoza.

## Moment 5 – ALM

Solutions pojawiają się dopiero wtedy, gdy uczestnicy mają już realne komponenty do przeniesienia między środowiskami.
