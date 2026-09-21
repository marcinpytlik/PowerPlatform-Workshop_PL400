# Power Apps i formularze SharePoint Online

## Cel dokumentu

Dokument porównuje trzy podejścia do budowania formularzy i aplikacji związanych z SharePoint Online.

## 1. Standardowy formularz SharePoint

Najprostsze rozwiązanie.

Dobre dla:

- prostych list,
- małej liczby pól,
- niewielkiej logiki,
- standardowego UX.

## 2. Customize Forms w Power Apps

Pozwala zastąpić standardowy formularz listy formularzem Power Apps.

Zalety:

- szybkie dostosowanie UX,
- Power Fx,
- walidacja,
- warunkowe sekcje.

Ograniczenie:

- formularz pozostaje silnie związany z konkretną listą SharePoint.

## 3. Standalone Canvas App

Jest niezależną aplikacją korzystającą z SharePoint jako źródła danych.

Daje większą kontrolę nad:

- ekranami,
- nawigacją,
- procesem użytkownika,
- wieloma źródłami danych.

## 4. SPFx Form Customizer

Pozwala zbudować własny formularz dla listy przy użyciu SPFx.

Ma sens, gdy potrzebna jest większa kontrola niż w Power Apps i zespół akceptuje custom development.

## 5. Porównanie

| Scenariusz | Kierunek |
|---|---|
| prosty formularz | standardowy SharePoint |
| szybka personalizacja formularza | Customize Forms |
| pełna aplikacja biznesowa | Canvas App |
| bardzo niestandardowy formularz w SharePoint | SPFx Form Customizer |

## 6. Lifecycle

Customize Forms jest ściśle związany z listą.

Standalone Canvas App ma własny lifecycle i może korzystać z wielu źródeł.

SPFx wymaga klasycznego lifecycle developerskiego.

## 7. Ryzyka

- ukryta logika w wielu właściwościach kontrolek,
- silne związanie z konkretną listą,
- problematyczne późniejsze przejście do Dataverse,
- brak jawnego podziału UI / process / data.

## 8. Rekomendacja

Im bardziej formularz zaczyna przypominać wieloekranową aplikację, tym bardziej warto rozważyć standalone Canvas App zamiast dalszego rozbudowywania Customize Forms.
