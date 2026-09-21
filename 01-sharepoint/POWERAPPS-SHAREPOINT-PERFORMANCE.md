# Power Apps + SharePoint Online – wydajność

## Cel dokumentu

Dokument opisuje najczęstsze przyczyny problemów wydajnościowych Canvas Apps korzystających z SharePoint Online.

## 1. Najważniejsza zasada

Wydajność aplikacji zależy nie tylko od liczby rekordów, ale także od liczby requestów, szerokości danych, liczby zależności i sposobu wykonywania formuł.

## 2. N+1

Klasyczny wzorzec:

```text
Gallery
  |
  +--> row 1 -> LookUp
  +--> row 2 -> LookUp
  +--> row 3 -> LookUp
  ...
```

100 rekordów w galerii może wygenerować dziesiątki lub setki dodatkowych wywołań.

## 3. App.OnStart

Duży `App.OnStart` wydłuża uruchamianie aplikacji.

Nie należy ładować wszystkich list i słowników tylko dlatego, że mogą być potrzebne później.

## 4. Lazy loading

Dane powinny być pobierane wtedy, gdy użytkownik rzeczywiście ich potrzebuje.

Przykład:

```text
Start aplikacji
  -> minimum konfiguracji

Wejście na ekran Contracts
  -> dane Contracts

Otwarcie szczegółów
  -> dane powiązane
```

## 5. Refresh

Nadmierne `Refresh()` zwiększa liczbę requestów i może pogarszać UX.

Po zapisie nie zawsze trzeba odświeżać całe źródło.

## 6. Cross-screen references

Odwołania do kontrolek na innych ekranach zwiększają sprzężenie i mogą powodować wcześniejsze ładowanie ekranów.

Lepiej przekazywać dane jawnie przez parametry nawigacji lub stan aplikacji.

## 7. Szerokie listy

Lista z dużą liczbą kolumn zwiększa ilość przesyłanych danych.

Jeżeli aplikacja potrzebuje 8 pól z tabeli zawierającej 100 kolumn, warto ograniczyć zakres danych i uprościć model.

## 8. Kolekcje

Kolekcje mogą poprawić UX dla małych, stabilnych zestawów danych.

Nie powinny być używane jako domyślny cache całej listy produkcyjnej.

## 9. Gallery + złożone formuły

Każda ciężka formuła wykonywana per row jest mnożona przez liczbę elementów galerii.

Szczególnej uwagi wymagają:

- `LookUp`,
- złożone `If`,
- operacje na wielu źródłach,
- obliczenia tekstowe,
- wywołania connectorów.

## 10. Live Monitor

Live Monitor pozwala analizować:

- requesty,
- duration,
- błędy,
- Trace,
- częstotliwość wywołań connectorów.

Jest podstawowym narzędziem do identyfikowania nadmiarowych requestów i problemów N+1.

## 11. Trace

`Trace()` pomaga korelować zachowanie aplikacji z działaniami użytkownika.

Przykład:

```powerfx
Trace("Contract saved")
```

## 12. Performance vs correctness

Niektóre optymalizacje mogą ukryć problemy poprawności.

Przykład:

```text
ClearCollect całej listy
```

może przyspieszyć późniejsze odczyty, ale przestaje być bezpieczne przy dużych listach i zmianach danych.

## 13. Anti-patterny

- Ładowanie wszystkiego przy starcie.
- Pełne `Refresh()` po każdej operacji.
- LookUp per row.
- Cross-screen references.
- Zbyt duża liczba globalnych zmiennych.
- Zbyt szerokie listy.
- Brak testów na większym wolumenie.

## 14. Checklista

- Czy formuły są delegowalne?
- Ile requestów wykonuje jeden ekran?
- Czy dane są pobierane tylko wtedy, gdy są potrzebne?
- Czy galeria generuje N+1?
- Czy Refresh jest konieczny?
- Czy aplikacja ładuje dane z innych ekranów?
- Czy Live Monitor potwierdza problem?

## 15. Dokumentacja

- https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/create-performant-apps-overview
- https://learn.microsoft.com/en-us/power-apps/maker/monitor-canvasapps
