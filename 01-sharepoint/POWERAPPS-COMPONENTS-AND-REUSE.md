# Power Apps – komponenty i ponowne użycie

## Cel

Dokument opisuje sposób ograniczania kopiowania logiki i UI w Canvas App.

## 1. Kiedy tworzyć komponent

Komponent ma sens, gdy element:

- występuje na wielu ekranach,
- ma spójny wygląd,
- ma własny kontrakt wejścia/wyjścia,
- powinien być utrzymywany w jednym miejscu.

Przykłady:

- nagłówek,
- menu,
- breadcrumb,
- dialog potwierdzenia,
- komunikat błędu,
- status badge,
- pagination control.

## 2. Input properties

Komponent powinien otrzymywać dane przez jawne właściwości wejściowe.

Przykład koncepcyjny:

```text
ContractStatusBadge.Status = ThisItem.Status.Value
```

## 3. Output / behavior

Nie ukrywaj skomplikowanej logiki biznesowej wewnątrz komponentu UI.

Komponent powinien komunikować zdarzenia i wartości, a logika domenowa powinna pozostawać jawna.

## 4. Component Library

Component Library jest przydatna, gdy wiele aplikacji ma współdzielić ten sam UI.

Wymaga jednak lifecycle:

- wersjonowanie,
- publikację,
- kompatybilność,
- właściciela.

## 5. Kopiowanie ekranów

Kopiowanie całego ekranu jest szybkie, ale zwiększa koszt utrzymania.

Jeżeli ta sama zmiana musi być wykonana w pięciu miejscach, prawdopodobnie brakuje warstwy reusable.

## 6. Wspólne funkcje

Power Fx nie jest klasycznym językiem z bibliotekami funkcji w takim sensie jak C#.

Do ograniczania powtórzeń wykorzystuj:

- komponenty,
- named formulas,
- `With()`,
- flow dla operacji backendowych,
- centralne dane konfiguracyjne.

## 7. Konfiguracja zamiast hard-code

Zamiast:

```powerfx
If(
    varEnvironment = "TEST",
    "https://...",
    "https://..."
)
```

preferuj environment variables lub konfigurację rozwiązania, jeśli aplikacja jest przenoszona pomiędzy środowiskami.

## 8. Granice komponentu

Komponent UI nie powinien:

- posiadać sekretów,
- zastępować security backendu,
- wykonywać złożonego workflow,
- zawierać całej logiki procesu biznesowego.

## 9. Zasada

Reusable element powinien posiadać mały, czytelny kontrakt i ograniczoną odpowiedzialność.
