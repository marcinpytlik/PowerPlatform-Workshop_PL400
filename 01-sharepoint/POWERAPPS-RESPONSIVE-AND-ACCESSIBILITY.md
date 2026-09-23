# Power Apps – responsive design i accessibility

## Cel

Dokument opisuje techniczne zasady budowy Canvas App działającej na różnych rozmiarach ekranu i dostępnej dla użytkowników korzystających z klawiatury lub technologii asystujących.

## 1. Kontenery

Preferuj layout containers zamiast ręcznego ustawiania każdego elementu przez stałe współrzędne.

```text
Vertical container
  Header
  Filters
  Gallery
  Footer
```

## 2. Rozmiar zależny od Parent

Przykład:

```powerfx
Width = Parent.Width
```

Zamiast stałego:

```powerfx
Width = 1366
```

## 3. Breakpoints

Przy dużych różnicach rozmiaru ekranu można przełączać układ:

```powerfx
If(
    App.Width < 768,
    Layout.Vertical,
    Layout.Horizontal
)
```

## 4. Gallery

Dla małych ekranów ogranicz liczbę pól widocznych jednocześnie.

Nie próbuj odwzorowywać tabeli desktopowej 1:1 na telefonie.

## 5. Font i skalowanie

Nie używaj mikroskopijnych fontów tylko po to, aby zmieścić więcej danych.

Układ powinien skalować się przez reorganizację, nie przez zmniejszanie wszystkiego.

## 6. AccessibleLabel

Interaktywne kontrolki powinny posiadać czytelne etykiety dostępności.

```powerfx
AccessibleLabel = "Wyślij kontrakt do akceptacji"
```

## 7. Klawiatura i kolejność

Sprawdź:

- tab order,
- fokus,
- możliwość obsługi bez myszy,
- czy ukryte kontrolki nie przechwytują fokusu.

## 8. Kolor nie może być jedyną informacją

Nie oznaczaj statusu wyłącznie kolorem.

Zamiast:

```text
czerwony / zielony
```

użyj:

```text
Rejected + kolor
Approved + kolor
```

## 9. Komunikaty błędów

Błąd powinien wskazywać:

- co jest niepoprawne,
- gdzie,
- jak poprawić.

Nie wystarczy czerwone obramowanie.

## 10. Test

Przed publikacją sprawdź aplikację:

- desktop,
- mniejszy laptop,
- tablet,
- klawiatura bez myszy,
- powiększenie przeglądarki,
- App Checker accessibility.

## 11. Zasada

Responsive design i accessibility są częścią architektury UI, a nie poprawką wykonywaną na końcu projektu.
