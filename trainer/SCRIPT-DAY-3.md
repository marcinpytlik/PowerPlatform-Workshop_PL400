# Skrypt dnia 3 – jakość, diagnostyka, ALM, deployment

**Cel dnia:** uczestnik umie zdiagnozować incydent, zapisać błąd do Process Log i przenieść Solution DEV → TEST.

**Laby obowiązkowe:** 09, 10, 12, 13 (wariant skrócony).
**LAB 11:** wariant 30–45 min, nie pełne 90.
**Monitor:** krótki blok przed wydajnością.
**Teoria:** [THEORY-TALK-TRACK](THEORY-TALK-TRACK.md) dzień 3. Nie wykładaj sagi ani circuit breakera.

## Przygotowanie (08:40)

- mock API w trybie `success`,
- TEST puste albo z poprzedniej wersji, którą wolno nadpisać,
- jeden wcześniej przygotowany incydent do LAB 10 – patrz [DEMO-FAILURES](DEMO-FAILURES.md),
- support email = skrzynka szkoleniowa.

---

## 09:00–10:15 – LAB 09 error handling (75 min)

Zaczynaj od kopii `VCM - Contract Submitted` zapisanej jako `VCM - Contract Submitted - v2`. Nie edytuj jedynej działającej wersji i nie wracaj do flow SharePoint.

Demo 15 min: Scope TRY / CATCH / FINALLY i Run after. Potem uczestnicy mapują Process Log.

Wymuś kolejność testów:

1. `201` – CATCH skipped, FINALLY działa,
2. `x-mock-mode: 500` albo numer `.../500` – ProcessLog + `Integration Error`,
3. `Terminate Failed` **po** FINALLY.

Nie kończ CATCH akcją Terminate – to najczęstszy błąd sali.

**Checkpoint:** jest rekord Process Log z Flow Run ID i Correlation ID.

**Talk track:** TRY/CATCH/FINALLY, business vs technical, append-only log. `Needs Manual Review` to pomysł recovery, nie nowy Choice do modelu VCM.

---

## 10:15–11:15 – LAB 10 troubleshooting (60 min)

Jeden wariant na całą salę. Rekomendacja: **stale write** albo **trigger loop** – najłatwiej je pokazać.

Zasada, którą powtarzasz na głos:

> Nie edytujemy flow, dopóki nie ma root cause w jednym zdaniu.

15 min ciszy na timeline. Potem wspólne porównanie. Fix dopiero po Twoim „ok”.

Szczegóły odtworzenia: [DEMO-FAILURES](DEMO-FAILURES.md).

**Checkpoint:** uczestnik ma wypełniony raport incydentu, nie tylko „naprawiłem status”.

**Talk track (5 min):** Observability. Na tablicy: Business ID + Correlation ID + Flow Run ID + Process Log.

---

## 11:15–11:30 – Przerwa

---

## 11:30–12:00 – Monitor

Z LAB 11 weź tylko zadanie Monitor:

- otwarcie listy, filtr, zapis,
- znalezienie najdroższego requestu,
- odnalezienie `Trace("Contract saved")`, jeśli ktoś dodał je w dniu 1.

To jest pomost do wydajności, nie osobny lab.

---

## 12:00–12:30 – LAB 11 wariant skrócony (30 min)

Na sali tylko:

1. zły flow: Get items bez filtra + Apply to each + Condition,
2. ten sam flow z Filter Query,
3. jedna niedelegowalna formuła w Canvas i wniosek: brak błędu ≠ poprawny wynik.

Reszta labu (indeks, concurrency, 50 000 rekordów) jest materiałem własnym albo dniem 4.

**Checkpoint:** liczba rekordów i czas spadły po Filter Query.

**Talk track:** Delegation First, Lazy Loading, N+1. Brak błędu ≠ poprawny wynik.

---

## 12:30–13:00 – Lunch

W tym czasie prowadzący ustawia mock API z powrotem na `success` i sprawdza, czy TEST żyje.

---

## 13:00–14:15 – LAB 12 Solutions (75 min)

Nie twórz drugiego Solution. Podnieś wersję istniejącego do `1.0.0.0`.

Kolejność:

1. inwentaryzacja komponentów,
2. Connection References,
3. Environment Variables i usunięcie hard-code URL / maila,
4. Solution Checker jeśli jest,
5. rysunek child flows – implementuj podział tylko gdy grupa ma bufor.

Jeżeli child flows nie przejdą: zostaje jeden orchestrator, ale URL jest w zmiennej środowiskowej. To wystarczy do LAB 13.

**Checkpoint:** `VCM_API_BASE_URL` nie siedzi w akcji HTTP jako literał.

**Talk track:** Configuration over Hard-code, Environment Variables, Connection References. Solution jest przenośnym artefaktem, nie kopią DEV.

---

## 14:15–15:15 – LAB 13 wariant skrócony (60 min)

Uczestnicy nie robią pełnego E2E każdy u siebie.

| Kto | Co |
|---|---|
| Wszyscy | pre-check, export managed `1.0.0.0` |
| Wszyscy albo pary | import do TEST, connection references, env vars |
| Wszyscy | smoke: Model-driven + jedna umowa Draft |
| Prowadzący | E2E 150 000 i negative test 500 na rzutniku |

Pytanie stop: „Skąd wiesz, że jesteś w TEST?”

**Checkpoint:** managed Solution jest w TEST, `VCM_API_BASE_URL` wskazuje API testowe / szkoleniowe, nie URL z hard-code DEV.

---

## 15:15–15:45 – Ćwiczenia / Q&A

Weź 2 z puli: E02, E03, E06, E07. Odpowiedzi kierunkowe są w [EXPECTED-ANSWERS](../solutions/EXPECTED-ANSWERS.md).

Nie zaczynaj nowego labu.

---

## 15:45–16:00 – Podsumowanie

Wróć do architektury docelowej z README. Trzy reguły na tablicy:

1. Status biznesowy i status integracji to nie to samo.
2. Diagnoza przed poprawką.
3. Zmiana źródłowa powstaje w DEV i jedzie jako Solution.

---

## Jeśli dzień się wywróci

| Minimum | Można odpuścić |
|---|---|
| TRY/CATCH + ProcessLog | timeout, child flows |
| Jeden przeanalizowany incydent | własne odtworzenie wszystkich wariantów A–E |
| Export/import managed + smoke | E2E każdego uczestnika, Pipelines |

Deployment demo prowadzącego jest lepszy niż 12 niedokończonych importów.
