# LAB 10 – Troubleshooting: „flow zrobił coś kompletnie nieprzewidzianego”

## Cel laboratorium

Przeprowadzić pełną analizę incydentu bez zmieniania flow przed ustaleniem przyczyny.

## Czas

75–90 minut. W agendzie 3-dniowej: **60 min**, jeden wariant przygotowany przez prowadzącego. Nie odtwarzaj A–E na raz. Procedury: [`../trainer/DEMO-FAILURES.md`](../trainer/DEMO-FAILURES.md).

## Scenariusz

Użytkownik zgłasza:

> Umowa `VCM/2026/003` była Approved, ale po kilku minutach status sam wrócił do Submitted. Nikt nie wie dlaczego.

Twoim zadaniem nie jest „naprawić status”. Masz ustalić **kto, kiedy i dlaczego wykonał nieoczekiwany update**.

---

# Reguła laboratorium

**Nie edytuj flow do momentu zakończenia analizy.**

Najpierw zbierz dowody.

---

# Materiał incydentu

Prowadzący przygotowuje jeden z wariantów:

A. dwa flowy aktualizują ten sam rekord,
B. retry wykonuje powtórną operację,
C. trigger `When item is created or modified` uruchamia się po Update item,
D. starszy run kończy się później i nadpisuje nowszy stan,
E. równoległe gałęzie zapisują różne statusy.

---

# Zadanie 1 – Zidentyfikuj obiekt biznesowy

Zapisz:

```text
ContractNumber = VCM/2026/003
Contract ID = ...
CorrelationId = ...
Current status = Submitted
Modified = ...
Modified by = ...
```

Jeżeli korzystasz z Dataverse, sprawdź audit history. Jeżeli SharePoint – Version history.

Nie zaczynaj od Power Automate. Najpierw ustal fakt: **jaki zapis zmienił rekord**.

---

# Zadanie 2 – Zbuduj timeline

Utwórz tabelę:

| Timestamp | Źródło | Operacja | Status przed | Status po | CorrelationId |
|---|---|---|---|---|---|

Wpisuj kolejne zdarzenia podczas analizy.

Cel: na końcu timeline ma pokazać kolejność zdarzeń.

---

# Zadanie 3 – Znajdź runy

W Power Automate:

1. Otwórz flow odpowiedzialny za Contract.
2. Run history.
3. Ogranicz analizę do okna czasowego wokół `Modified`.
4. Otwórz wszystkie runy dotyczące Contract ID.
5. Dla każdego zapisz:
   - start time,
   - duration,
   - status,
   - correlation ID,
   - trigger payload Status.

Jeżeli runów jest kilka, nie zakładaj, że ostatnio rozpoczęty skończył się jako ostatni.

---

# Zadanie 4 – Trigger input

Dla każdego podejrzanego runu otwórz trigger i sprawdź Inputs/Outputs.

Zapisz:

```text
ID
Status
Modified
CorrelationId
Amount
```

Pytanie:

> Jaki status rekord miał w momencie uruchomienia tego runu?

---

# Zadanie 5 – Pierwszy nieoczekiwany update

W każdym runie znajdź akcje aktualizujące Contract.

Dla każdej akcji zanotuj:

```text
Action name
Start/end time
Target ID
Written Status
Written CorrelationId
Result
```

Szukamy **pierwszej operacji, która zapisała nieoczekiwaną wartość**, a nie ostatniego miejsca, gdzie widzimy błąd.

---

# Zadanie 6 – Retry

Otwórz podejrzaną akcję i sprawdź:

- Settings -> retry policy,
- historię prób, jeśli jest widoczna,
- czas między próbami,
- status API.

Pytanie:

> Czy retry mogło ponownie wykonać operację niebędącą idempotentną?

---

# Zadanie 7 – Concurrency

Sprawdź ustawienia triggera i pętli.

Zidentyfikuj:

- czy trigger ma concurrency control,
- czy Apply to each działa równolegle,
- czy istnieją parallel branches.

Narysuj:

```text
Run A start 10:00
   |
   +----- waiting for approval --------+
                                      |
Run B start 10:03                     |
   |                                  |
   +-- update Approved 10:04           |
                                      |
Run A resumes ------------------------+
   |
   +-- update Submitted 10:07  <-- stale write
```

Jeżeli ten wzorzec pasuje do incydentu, mamy klasyczny stale write/race condition.

---

# Zadanie 8 – Audit / Version History

## Dataverse

Sprawdź Audit History:

- old value,
- new value,
- changed by,
- changed on.

## SharePoint

Sprawdź Version History i wersję, która zmieniła Status.

Porównaj timestamp z Run History.

---

# Zadanie 9 – Root cause

Zapisz jednozdaniową przyczynę w formacie:

```text
Status został nadpisany przez <flow/run>, ponieważ <mechanizm>, co było możliwe dlatego, że <brak zabezpieczenia>.
```

Przykład:

```text
Status został nadpisany przez starszy run procesu approval, ponieważ run wznowił się po późniejszym zapisie i bez sprawdzenia bieżącej wartości wykonał Update Contract.
```

---

# Zadanie 10 – Zabezpieczenie

Dobierz minimum dwa zabezpieczenia, np.:

- trigger conditions,
- sprawdzenie aktualnego statusu przed update,
- optimistic concurrency / ETag tam, gdzie wspierane,
- business state transition validation,
- concurrency control,
- idempotency key,
- osobne pole IntegrationStatus zamiast nadpisywania Status,
- child flow z jedną odpowiedzialnością,
- correlation ID,
- audyt/logowanie.

Nie wybieraj mechanizmu tylko dlatego, że „zadziałał w demo”. Uzasadnij.

---

# Zadanie 11 – Dopiero teraz popraw flow

Po zatwierdzeniu root cause przez prowadzącego:

1. skopiuj flow,
2. wprowadź wybrane zabezpieczenie,
3. odtwórz scenariusz,
4. potwierdź, że stary run nie może już nadpisać nowszego stanu.

---

# Raport incydentu

Uzupełnij:

```text
Incident:
Business object:
Time window:
Detected state:
Expected state:
First unexpected write:
Flow run ID:
Correlation ID:
Root cause:
Contributing factor:
Fix:
Prevention:
```

---

# Kryterium ukończenia

Uczestnik:

- potrafi znaleźć właściwy run,
- odtwarza timeline,
- znajduje pierwszy nieoczekiwany update,
- rozróżnia symptom od root cause,
- wskazuje mechanizm race/retry/trigger loop,
- proponuje trwałe zabezpieczenie.

---

# Materiał Microsoft

- Troubleshoot Power Automate triggers: https://learn.microsoft.com/en-us/troubleshoot/power-platform/power-automate/flow-run-issues/triggers-troubleshoot
- Error handling guidance: https://learn.microsoft.com/en-us/power-automate/guidance/coding-guidelines/error-handling
