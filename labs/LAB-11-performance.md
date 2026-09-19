# LAB 11 – Performance i limity: SharePoint, Canvas App i Power Automate

## Wariant na sali (30 min)

W agendzie 3-dniowej nie robimy pełnych 90 minut.

Obowiązkowe:

1. zadanie 1 – zły Get items + Apply to each + Condition,
2. zadanie 2 – Filter Query i porównanie czasu,
3. zadanie 5 – jedna niedelegowalna formuła: brak błędu ≠ poprawny wynik.

Monitor jest osobnym blokiem 11:30–12:00 (zadanie 7). Zadania 3, 4, 6, 8–10 zostają jako materiał własny albo dzień 4.

## Cel laboratorium

Porównać rozwiązanie „działa” z rozwiązaniem „skaluje się rozsądnie”. Uczestnicy wykonują pomiar przed i po zmianie.

## Czas

90 minut.

## Wymagania

- lista Contracts zawierająca większy zestaw danych – rekomendowane 500–5000 rekordów szkoleniowych,
- Canvas App,
- flow Power Automate.

---

# Zasada przewodnia

```text
Filtruj możliwie blisko źródła.
Pobieraj tylko dane, których potrzebujesz.
Nie rozwiązuj limitów przez przenoszenie całego datasetu do klienta.
```

---

# Część A – Power Automate

## Zadanie 1 – Wersja celowo zła

Utwórz flow testowy:

```text
VCM - Performance Baseline
```

Trigger: Manual.

Dodaj:

```text
Get items - Contracts
```

Bez Filter Query.

Następnie:

```text
Apply to each
  -> Condition Status = Approved
       -> Compose ContractNumber
```

Uruchom i zanotuj:

- duration całego flow,
- duration Get items,
- liczbę pobranych rekordów,
- liczbę iteracji,
- liczbę akcji wykonanych w pętli.

Wpisz wynik:

```text
BASELINE
Records returned:
Loop iterations:
Duration:
```

---

# Zadanie 2 – Filter Query

Skopiuj flow do:

```text
VCM - Performance Optimized
```

Usuń Condition z pętli.

W `Get items` ustaw OData Filter Query dla statusu Approved zgodnie z rzeczywistą nazwą pola SharePoint.

Przykładowa idea:

```text
Status eq 'Approved'
```

> Dla kolumn Choice format zapytania może zależeć od konektora i wewnętrznej nazwy kolumny. Sprawdź wynik w swoim tenantcie.

Uruchom ponownie.

Zapisz:

```text
OPTIMIZED
Records returned:
Loop iterations:
Duration:
```

Porównaj.

---

# Zadanie 3 – Top count i Select Query

Jeżeli scenariusz biznesowy potrzebuje np. tylko 100 rekordów:

1. ustaw Top Count,
2. jeżeli connector udostępnia Limit columns by view, utwórz widok zawierający tylko potrzebne kolumny i użyj go,
3. sprawdź rozmiar odpowiedzi.

Omów różnicę między:

- Top Count,
- pagination threshold,
- logicznym warunkiem biznesowym.

Nie zwiększaj pagination bez uzasadnienia tylko po to, aby „zniknął limit”.

---

# Zadanie 4 – Indeks SharePoint

Sprawdź, czy kolumna Status jest indeksowana.

Usuń indeks tylko w środowisku demonstracyjnym, jeżeli prowadzący przygotował bezpieczny dataset, i porównaj zachowanie zapytań. Następnie przywróć indeks.

Omów List View Threshold i znaczenie projektowania filtrów dla dużych list.

---

# Część B – Canvas App

# Zadanie 5 – Delegation

Otwórz `VCM - Contract Portal`.

Ustaw limit danych dla niedelegowalnych zapytań na niską wartość szkoleniową, np. 100, jeśli środowisko na to pozwala.

Utwórz celowo niedelegowalną formułę lub znajdź istniejące ostrzeżenie.

Następnie:

1. uruchom aplikację,
2. wyszukaj rekord poza pierwszym zestawem lokalnym,
3. sprawdź, czy aplikacja zwraca poprawny wynik.

Cel: pokazać, że brak błędu wykonania nie oznacza poprawności wyniku.

---

# Zadanie 6 – Nie ładuj wszystkiego do kolekcji

Porównaj:

```powerfx
ClearCollect(colContracts, Contracts)
```

z używaniem delegowalnego filtra bezpośrednio na datasource.

Omów:

- czas startu aplikacji,
- pamięć klienta,
- niepełny dataset,
- odświeżanie danych,
- spójność.

---

# Zadanie 7 – Monitor

Uruchom **Monitor** dla Canvas App zgodnie z bieżącym interfejsem Power Apps.

1. Start Monitor/Live Monitor.
2. Otwórz aplikację w sesji monitorowanej.
3. Wykonaj:
   - otwarcie listy,
   - wyszukiwanie,
   - zmianę filtra,
   - otwarcie szczegółów,
   - zapis formularza.
4. Znajdź requesty do SharePoint/Dataverse.
5. Zidentyfikuj najdroższą operację.

Jeżeli w aplikacji użyto `Trace()`, znajdź zdarzenie `Contract saved`.

---

# Część C – Limity i throttling

# Zadanie 8 – 429

Wróć do scenariusza z LAB 04.

Odpowiedz:

1. Która warstwa zwróciła 429 – Power Platform, connector czy API zewnętrzne?
2. Czy Retry-After jest dostępne?
3. Czy retry jest bezpieczne?
4. Czy można zmniejszyć liczbę requestów zamiast zwiększać liczbę retry?

---

# Zadanie 9 – Concurrency

Dla Apply to each:

1. sprawdź ustawienia concurrency,
2. zanotuj domyślne zachowanie,
3. wykonaj test z kontrolowaną współbieżnością, jeśli prowadzący na to pozwala,
4. porównaj duration.

Omów trade-off:

```text
większa concurrency -> szybciej
ale
większa concurrency -> więcej równoczesnych requestów -> większe ryzyko throttlingu/race condition
```

---

# Zadanie 10 – Raport porównawczy

Uzupełnij:

| Metryka | Before | After |
|---|---:|---:|
| Records returned | | |
| Loop iterations | | |
| Flow duration | | |
| Requests / actions | | |
| Delegation warning | | |

Dopisz wniosek maksymalnie w trzech zdaniach.

---

# Kryterium ukończenia

- filtr został przeniesiony do Get items,
- liczba pobranych rekordów spadła,
- uczestnik potrafi znaleźć delegation warning,
- uczestnik potrafi uruchomić Monitor,
- potrafi wyjaśnić Top Count vs pagination,
- potrafi wyjaśnić wpływ concurrency na throttling.

---

# Materiał Microsoft

- Power Automate limits: https://learn.microsoft.com/en-us/power-automate/limits-and-config
- SharePoint connector: https://learn.microsoft.com/en-us/connectors/sharepointonline/
