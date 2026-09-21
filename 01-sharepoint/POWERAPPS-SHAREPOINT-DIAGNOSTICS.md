# Power Apps + SharePoint Online – diagnostyka

## Cel dokumentu

Dokument porządkuje narzędzia i źródła danych używane do diagnozowania aplikacji Power Apps współpracujących z SharePoint i Power Automate.

## 1. App Checker

App Checker pomaga wykrywać:

- błędy formuł,
- ostrzeżenia,
- problemy dostępności,
- część problemów wydajnościowych.

Nie zastępuje testów runtime.

## 2. Live Monitor

Live Monitor pozwala obserwować:

- requesty,
- response,
- czas trwania,
- connector calls,
- błędy,
- Trace.

Jest podstawowym narzędziem do diagnostyki runtime Canvas App.

## 3. Trace

`Trace()` pozwala dodać własne zdarzenia diagnostyczne.

Przykład:

```powerfx
Trace("Submit Contract started")
```

## 4. Power Automate Run History

Run History pokazuje:

- trigger,
- input/output akcji,
- czas wykonania,
- status,
- retry,
- błędy.

Dla procesu wieloflowowego powinien być uzupełniony correlation ID.

## 5. SharePoint Version History

Version History pozwala ustalić:

- kto zmienił rekord,
- kiedy,
- jakie wartości uległy zmianie.

Jest szczególnie przydatny przy podejrzeniu nadpisania danych lub trigger loop.

## 6. Correlation ID

Własny identyfikator procesu pozwala połączyć:

```text
Canvas App
Power Automate
SharePoint
API
Process Log
```

w jeden timeline.

## 7. Browser DevTools

Network trace może pomóc przy:

- błędach HTTP,
- problemach ładowania zasobów,
- nieoczekiwanych requestach,
- diagnostyce SPFx.

## 8. Diagnostyka krok po kroku

```text
1. Symptom
2. Timeline
3. Evidence
4. Hypothesis
5. Root Cause
6. Fix
```

Nie należy rozpoczynać od losowej modyfikacji formuł.

## 9. Typowe symptomy

### "Aplikacja jest wolna"

Sprawdzić:

- liczba requestów,
- N+1,
- Refresh,
- OnStart,
- niedelegowalne formuły.

### "Rekord zniknął"

Sprawdzić:

- delegation,
- filtry,
- permissions,
- version history.

### "Flow uruchomił się dwa razy"

Sprawdzić:

- trigger,
- Update item,
- trigger conditions,
- correlation ID.

### "Działa u mnie, nie działa u użytkownika"

Sprawdzić:

- sharing aplikacji,
- SharePoint permissions,
- connection,
- DLP,
- role użytkownika.

## 10. Zasada

Najpierw należy zebrać dowody i odtworzyć timeline. Dopiero później zmieniać rozwiązanie.
