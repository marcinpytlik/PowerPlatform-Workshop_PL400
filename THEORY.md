# Teoria – Power Platform Advanced Workshop

Ten katalog wiedzy uzupełnia LAB-y o **zasady projektowania, wzorce i antywzorce**.

Nie chodzi o zapamiętanie listy nazw. Celem jest nauczenie uczestnika podejmowania decyzji:

- gdzie umieścić logikę,
- jak ograniczać sprzężenie,
- jak projektować przepływ danych,
- jak przygotować rozwiązanie na błędy,
- jak zachować możliwość rozwoju i utrzymania.

## Materiały

### Architektura całego rozwiązania

[POWER-PLATFORM-PATTERNS](00-architecture/POWER-PLATFORM-PATTERNS.md)

Tematy: Thin UI / Smart Backend, CRUD App, Workflow-backed App, Model-driven Administration, Event-driven thinking, State Machine, Source of Truth, Sync vs Async, Configuration, Strangler Migration, Anti-corruption Layer, Observability, Failure Isolation i decision matrix.

### Power Apps / Canvas Apps

[DESIGN-PATTERNS – Power Apps](02-canvas-app/DESIGN-PATTERNS.md)

Tematy: Separation of Concerns, Screen as a Feature, Navigation Parameters, State Management, Form Pattern, Delegation First, Server-side over Client-side, reusable components, configuration over hard-code, optimistic vs confirmed state, error boundaries, lazy loading, naming conventions i anti-patterns.

### Power Automate

[DESIGN-PATTERNS – Power Automate](03-power-automate/DESIGN-PATTERNS.md)

Tematy: Orchestrator, Child Flows, Single Responsibility, Trigger Guard, Idempotency, Retry classification, TRY/CATCH/FINALLY, business vs technical errors, Correlation ID, append-only Process Log, configuration, async processing, fan-out/fan-in, saga-like processes, compensating actions, circuit breaker concept i dead-letter/manual intervention.

---

# Jak używać tych materiałów na szkoleniu

Na sali obowiązuje [`trainer/THEORY-TALK-TRACK.md`](trainer/THEORY-TALK-TRACK.md) oraz momenty wpisane w [`00-agenda/AGENDA.md`](00-agenda/AGENDA.md) i `trainer/SCRIPT-DAY-*.md`. Ten plik jest indeksem i appendixem – nie skryptem wykładu.

Nie wykładaj wszystkich wzorców naraz. Najlepszy moment to sytuacja, gdy uczestnicy **najpierw zobaczą problem**, a potem nazwiesz rozwiązanie.

~~~text
najpierw kopiujemy Approval trzy razy
        ↓
robi się dużo powtarzalnej logiki
        ↓
dopiero wtedy pokazujemy Child Flow Pattern
~~~

Podobnie:

~~~text
najpierw SharePoint prototype
        ↓
pojawiają się ograniczenia
        ↓
dopiero wtedy Strangler Migration do Dataverse
~~~

To pozwala uczestnikowi zrozumieć **po co istnieje wzorzec**, a nie tylko zapamiętać jego nazwę.