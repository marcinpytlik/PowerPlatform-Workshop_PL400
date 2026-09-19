# Theory Talk Track – ściąga prowadzącego

Używaj tego pliku z [AGENDA](../00-agenda/AGENDA.md) i skryptów dnia. Pełne opisy wzorców są w [THEORY.md](../THEORY.md). Saga, circuit breaker, anti-corruption i compensating action są appendixem – tylko na pytanie albo dzień 4.

## Dzień 1

### Po LAB 02 – Canvas App

5–10 minut: Separation of Concerns, Screen as a Feature, State Management, Delegation First, Server-side over Client-side.

**Pytanie do grupy:** Co się stanie, jeśli całą logikę procesu umieścimy w OnSelect przycisku?

### Po LAB 03 – pierwszy flow

10 minut: Trigger Guard, Single Responsibility, Idempotency, correlation ID.

**Pytanie:** Co się stanie, jeśli Update item uruchomi ten sam flow drugi raz?

### Po LAB 04 – HTTP

10 minut: retry classification, business vs technical error, idempotency, failure isolation.

**Pytanie:** Czy HTTP 409 i HTTP 500 powinny mieć ten sam retry policy?

---

# Dzień 2

### Przed LAB 05

10 minut: Source of Truth, State Machine, relacje zamiast ręcznego sklejania danych.

### LAB 06 – migracja

Najważniejszy wzorzec: **Strangler Migration Pattern**

~~~text
stary model działa
   ↓
budujemy nowy model obok
   ↓
przepinamy komponent po komponencie
   ↓
test regresyjny
   ↓
wyłączamy stary proces
~~~

### Po LAB 07

5 minut: **Model-driven Administration Pattern**. Canvas App i Model-driven App nie konkurują ze sobą. Obsługują różne role i potrzeby.

### Projekt refaktoryzacji flow

15 minut: Orchestrator, Child Flow, Single Responsibility, Configuration over Hard-code.

---

# Dzień 3

### Error handling

10 minut: TRY/CATCH/FINALLY, business vs technical errors, append-only log, dead-letter/manual intervention.

### Troubleshooting

5 minut: Observability, correlation ID, Source of Truth.

### Performance

10 minut: Delegation First, Lazy Loading, N+1, server-side processing.

### ALM

10 minut: Configuration over Hard-code, Environment Variables, Connection References, rozwiązanie jako przenośny artefakt.

---

# Wzorce, które warto narysować na tablicy

## 1. Thin UI
~~~text
UI -> Data -> Workflow/API
~~~

## 2. Orchestrator
~~~text
Trigger
  |
  v
Orchestrator
 /   |    \
A    B     C
~~~

## 3. State Machine
~~~text
Draft -> Submitted -> In Approval -> Approved -> Integration Pending
                              |                         |
                              v                         +--> Integrated
                           Rejected                     +--> Integration Error
~~~

## 4. Retry classification
~~~text
429 / transient 5xx -> retry
400 / 409 business -> no blind retry
~~~

## 5. Observability
~~~text
Business ID
+ Correlation ID
+ Flow Run ID
+ Process Log
~~~

---

# Zdanie, które spina cały warsztat

> Low-code nie zwalnia z projektowania. Im łatwiej coś zbudować, tym łatwiej również szybko zbudować rozwiązanie trudne do utrzymania.