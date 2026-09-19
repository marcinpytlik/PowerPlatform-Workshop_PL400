# Skrypt dnia 1 – od pomysłu do działającej aplikacji

**Cel dnia:** uczestnik ma działający prototyp SharePoint + Canvas + Approval i rozumie, dlaczego ten model zaczyna boleć.

**Laby:** 01, 02, 03, 04.
**Nie ruszamy:** Dataverse, Solution, wielojęzyczność.

## Przygotowanie (08:30–09:00)

- mock API: `curl -s <URL>/health`,
- próbny approval na koncie prowadzącego,
- na tablicy: DEV, SharePoint, API URL, aliasy approverów,
- uczestnicy potwierdzają środowisko `VCM-DEV`.

Jeżeli HTTP albo Approvals padają – od razu [PLAN-B](PLAN-B.md), nie w trakcie LAB 04.

---

## 09:00–09:25 – Wprowadzenie i architektura

Pokaż proces biznesowy z [REQUIREMENTS](../00-architecture/REQUIREMENTS.md). Jedno zdanie na rolę.

Narysuj architekturę **początkową**, nie docelową:

```text
Canvas App -> SharePoint -> Power Automate -> Approval
```

Powiedz wprost: dzień 1 buduje prototyp, którego nie będziemy bronić jako rozwiązania produkcyjnego.

**Nie pokazuj** jeszcze Solution ani Dataverse. Zostaw napięcie.

---

## 09:25–10:35 – LAB 01 SharePoint (70 min)

Prowadzenie:

1. 10 min demo: lista Suppliers + Lookup na Contracts.
2. 50 min praca własna według labu.
3. 10 min pytania z końca LAB 01. Zostaw bez odpowiedzi „Dataverse to naprawi”. Wystarczy nazwać problem.

Skrót, gdy grupa jedzie wolno:

- prowadzący tworzy indeksy wspólnie,
- dane testowe wklejają z tabeli, nie wymyślają własnych numerów.

**Checkpoint:** trzy listy, pięć umów, Lookup działa.

---

## 10:35–10:50 – Przerwa

---

## 10:50–12:20 – LAB 02 Canvas App (90 min)

Demo 15 min: pusta aplikacja, trzy źródła, galeria, `Notify`.

Akcenty:

- `SubmitForm` + walidacja przed zapisem,
- `Trace()` – powiedzieć, że wrócimy do tego w dniu 3,
- niebieskie ostrzeżenie delegacji: zapisać, nie naprawiać przez `ClearCollect`.

Challenge `My contracts` tylko jeśli ktoś skończy 15 minut wcześniej.

**Checkpoint:** trzy ekrany, nowa umowa ląduje na liście SharePoint.

---

## 12:20–12:50 – Lunch

---

## 12:50–14:20 – LAB 03 pierwszy flow (90 min)

To jest najtrudniejszy blok dnia. Approval zjada czas.

Demo 20 min:

- trigger SharePoint,
- warunek `Status = Submitted`,
- Compose `guid()`,
- `Update item` -> drugi run. Zostaw ten drugi run na później (LAB 10).

Potem uczestnicy dokładają Finance / Legal / Management.

Jeżeli Approvals nie dochodzą do 13:20 – przełącz na plan B: ręczny status + email.

Testy A–D: nie każdy musi zrobić C (650 000). Minimum: 50 000 i jedno odrzucenie.

**Checkpoint:** umowa `Submitted` przechodzi w `In Approval`, odrzucenie kończy proces biznesowo.

---

## 14:20–14:35 – Przerwa

---

## 14:35–15:50 – LAB 04 HTTP (75 min)

Nie rób pełnej macierzy z każdym uczestnikiem. Prowadzący steruje trybami mock API.

Kolejność na sali:

| Minuty | Tryb | Co zobaczyć |
|---:|---|---|
| 0–15 | budowa requestu `supplierCode` + HTTP | payload w Compose |
| 15–30 | `201` | `ExternalSystemId`, Status `Integrated` |
| 30–45 | Settings: timeout `PT30S`, retry None, Secure outputs | security vs diagnosability |
| 45–60 | `409` i `500` | Run after, brak ślepego retry przy 409 |
| 60–75 | `429` None vs retry | jeden porównawczy run |

`timeout` i 400 zostaw jako demo prowadzącego, jeśli czas się sypie.

Przypomnienie kontraktu: ciało używa `supplierCode`, nie nazwy dostawcy. Numer `VCM/LAB04/429` sam wybiera tryb.

**Checkpoint:** uczestnik wskazuje Settings, Run after i różnicę 409 vs 500.

---

## 15:50–16:00 – Retrospekcja

Pytania na głos, odpowiedzi na tablicy:

1. Co już działa?
2. Gdzie SharePoint zaczyna przeszkadzać?
3. Co się stanie, gdy dwa flowy zapiszą ten sam Status?

Nie rozwiązuj. Powiedz: jutro migrujemy ten sam proces, nie budujemy drugiego.

## Jeśli dzień się wywróci

| Do godziny | Minimum, żeby dzień 2 miał sens |
|---|---|
| 14:20 | LAB 01–02 + trigger i jeden Approval |
| 15:50 | LAB 03 działa, HTTP jest wspólnym demo |
| 16:00 | przynajmniej jeden 201 i jeden 500 na sali |

Nie zaczynaj Dataverse „na 20 minut”. Lepiej dokończyć Approval.
