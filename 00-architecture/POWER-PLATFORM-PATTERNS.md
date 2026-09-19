# Power Platform – wzorce architektoniczne

## Cel

Ten dokument nie opisuje pojedynczego produktu. Pokazuje, jak podzielić odpowiedzialność pomiędzy Power Apps, Dataverse, Power Automate i API.

---

# 1. Thin UI / Smart Backend

```text
Power Apps
   |
   v
Dataverse
   |
   v
Power Automate / API
```

Power Apps odpowiada za doświadczenie użytkownika.

Procesy wieloetapowe, integracje i logika techniczna pozostają poza UI.

To jest domyślny kierunek dla VCM.

---

# 2. CRUD App Pattern

Najprostszy przypadek:

```text
Canvas App -> Dataverse
```

Dobre dla:

- formularzy,
- rejestrów,
- prostych aplikacji operacyjnych.

Nie dodawaj Power Automate tylko dlatego, że jest dostępny.

---

# 3. Workflow-backed App

```text
Canvas App
   |
   v
Dataverse
   |
   v
Power Automate
```

Dobre, gdy rekord rozpoczyna proces:

- approval,
- integrację,
- powiadomienia,
- generowanie dokumentów.

VCM jest przykładem tego wzorca.

---

# 4. Model-driven Administration Pattern

```text
Canvas App -> użytkownik biznesowy
Model-driven -> administrator / operator
          |
          v
       Dataverse
```

Nie każda rola potrzebuje tej samej aplikacji.

Canvas daje kontrolowane UX.

Model-driven daje szybki dostęp administracyjny do danych i relacji.

---

# 5. Event-driven Thinking

Zmiana stanu rekordu jest zdarzeniem biznesowym.

Przykład:

```text
Draft
  |
  v
Submitted
  |
  v
In Approval
```

Flow nie powinien zgadywać, co użytkownik miał na myśli.

Powinien reagować na jawny stan lub jawne zdarzenie.

---

# 6. State Machine Pattern

Proces modeluj jako przejścia pomiędzy stanami.

VCM:

```text
Draft
 -> Submitted
 -> In Approval
 -> Approved
 -> Integration Pending
 -> Integrated
```

Ścieżki alternatywne:

```text
In Approval -> Rejected
Integration Pending -> Integration Error
```

Zaleta: status procesu staje się obserwowalny i testowalny.

---

# 7. Source of Truth

Dla każdego typu informacji ustal jedno źródło prawdy.

Przykład:

```text
Contract state      -> Dataverse
Approval history    -> Approval table
Technical events    -> Process Log
Environment config  -> Environment Variables
Run diagnostics     -> Power Automate Run History
```

Nie przechowuj tego samego stanu w kilku miejscach bez jasno określonej synchronizacji.

---

# 8. Sync vs Async

## Synchronous

Użytkownik czeka na wynik.

Dobre dla:

- prostego zapisu,
- walidacji,
- szybkich operacji.

## Asynchronous

Użytkownik zapisuje żądanie, a proces wykonuje się w tle.

Dobre dla:

- approval,
- integracji,
- dokumentów,
- długich procesów.

VCM w większości powinien być asynchroniczny po `Submitted`.

---

# 9. Command vs State Change

## Command

```text
Submit Contract
```

## State change

```text
Status = Submitted
```

W low-code często używamy zmiany stanu rekordu jako komendy dla workflow.

Ważne jest, aby zrobić to świadomie i ograniczyć przypadkowe ponowne uruchomienia.

---

# 10. Configuration Pattern

Rozdziel:

```text
kod rozwiązania
od
konfiguracji środowiska
```

Konfiguracja:

- URL API,
- support email,
- feature flags,
- progi,
- identyfikatory.

Kod rozwiązania nie powinien się zmieniać tylko dlatego, że rozwiązanie trafiło z DEV do TEST.

---

# 11. Strangler Migration Pattern

To wzorzec szczególnie pasujący do naszego warsztatu.

Zamiast przepisać wszystko jednocześnie:

```text
SharePoint solution
      |
      v
stopniowa migracja
      |
      v
Dataverse solution
```

Migracja etapami:

1. przygotuj nowy model,
2. przenieś dane,
3. przepnij Canvas App,
4. przepnij flow,
5. test regresyjny,
6. wyłącz stary proces.

To ogranicza ryzyko dużej jednorazowej zmiany.

---

# 12. Anti-corruption Layer – koncepcja

Gdy zewnętrzny system ma inny model danych, nie rozlewaj jego formatu po całym rozwiązaniu.

Przykład:

```text
VCM Contract
   |
   v
Integration Flow / API mapping
   |
   v
External ERP contract
```

Warstwa integracyjna tłumaczy modele.

Dzięki temu zmiana ERP nie wymusza zmiany całej aplikacji.

---

# 13. Observability Pattern

Rozwiązanie produkcyjne powinno odpowiadać na pytania:

- co się wydarzyło?
- kiedy?
- dla którego rekordu?
- który flow?
- jaki Run ID?
- jaki correlation ID?
- jaki HTTP status?

Dlatego łączymy:

```text
Dataverse status
+ Process Log
+ Run History
+ correlation ID
```

---

# 14. Failure Isolation

Awaria jednego komponentu nie powinna bez potrzeby psuć całego procesu.

Przykład:

```text
approval succeeded
API succeeded
email failed
```

Nie zmieniaj Contract z `Integrated` na `Rejected` tylko dlatego, że notification nie zadziałało.

---

# 15. Decision matrix

| Potrzeba | Preferowany mechanizm |
|---|---|
| prosty CRUD | Power Apps + Dataverse |
| relacje, security, audit | Dataverse |
| wieloetapowy workflow | Power Automate |
| powtarzalna logika flow | Child Flow |
| ciężka logika obliczeniowa | API / Azure Function |
| szybki panel administracyjny | Model-driven App |
| pełna kontrola UX | Canvas App |
| konfiguracja środowiska | Environment Variables |
| historia biznesowa | Dataverse tables |
| diagnostyka techniczna | Process Log + Run History |
| duży wolumen / skomplikowana integracja | rozważ Logic Apps / Azure Functions |

---

# 16. Pytania architekta przed budową

1. Gdzie jest źródło prawdy?
2. Kto zmienia stan biznesowy?
3. Co dzieje się synchronicznie, a co asynchronicznie?
4. Co się stanie przy retry?
5. Czy operacja jest idempotentna?
6. Jak wygląda recovery?
7. Jak diagnozujemy pojedynczy przypadek?
8. Która konfiguracja zależy od środowiska?
9. Czy UI zna zbyt dużo szczegółów backendu?
10. Czy cały proces da się przetestować bez ręcznego „wiedzenia co kliknąć”?

---

# Materiały Microsoft

- Power Platform Architecture Center: https://learn.microsoft.com/en-us/power-platform/architecture/
- Power Apps reference architectures: https://learn.microsoft.com/en-us/power-platform/architecture/products/power-apps
- Power Automate reference architectures: https://learn.microsoft.com/en-us/power-platform/architecture/products/power-automate
