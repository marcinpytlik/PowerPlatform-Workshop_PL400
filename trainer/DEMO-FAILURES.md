# Kontrolowane awarie do demonstracji

Każda awaria ma: cel, przygotowanie, sygnał dla sali, oczekiwany root cause, fix dopiero po diagnozie.

Przed blokiem ustaw mock API na znany stan:

```bash
curl -s -X DELETE "$API/api/contracts"
curl -s -X PUT "$API/admin/mode" -H 'Content-Type: application/json' -d '{"mode":"success"}'
```

Nie łącz dwóch wariantów w jednym rekordzie.

---

## 1. Trigger loop

**Cel:** flow na create/modify sam siebie uruchamia przez `Update`.

**Gdzie:** LAB 03 / LAB 10, wariant C.

**Przygotowanie:**

1. Flow `When a row is added, modified or deleted` albo SharePoint `When an item is created or modified`.
2. Brak trigger condition.
3. Pierwsza akcja: `Update` Correlation ID albo Status.
4. Warunek `Status = Submitted` jest **po** update albo w ogóle go nie ma.

**Sygnał dla sali:**

> Uruchomiłem jedną zmianę, a w Run history są dwa albo trzy runy.

**Jak odtworzyć:**

1. Ustaw Contract na `Submitted` i zapisz.
2. Otwórz Run history w ciągu 30 sekund.
3. Pokazuj run 1: trigger Status=`Submitted`, potem Update na `In Approval`.
4. Pokazuj run 2: trigger Status=`In Approval`.

**Root cause:** trigger reaguje na własny zapis.

**Fix po diagnozie (minimum dwa):**

- trigger condition / warunek na Status,
- pole techniczne `ProcessState` albo porównanie starej i nowej wartości,
- nie oznaczaj runu biznesowego jako Failed.

---

## 2. 429 Too Many Requests

**Cel:** retry policy i pytanie o idempotencję.

**Gdzie:** LAB 04, LAB 11.

**Przygotowanie:** mock API żyje publicznie. Retry na HTTP ustawione na `None`, potem Exponential.

**Jak odtworzyć:**

```bash
# wariant A – jeden request
curl -i -X POST "$API/api/contracts" \
  -H 'Content-Type: application/json' \
  -H 'x-mock-mode: 429' \
  -d '{"contractNumber":"VCM/DEMO/429","supplierCode":"SUP-001","amount":1000,"currency":"PLN","correlationId":"demo-429"}'
```

Albo numer umowy `VCM/2026/429`.

W flow: ten sam POST, najpierw Retry = None, potem Retry włączone.

**Co zapisać z Run history:** liczba prób, czas, `Retry-After: 10`.

**Pytania, zanim pokażesz fix:**

- Czy każdą operację można ponowić?
- Co jeśli API zapisało rekord, a odpowiedź nie doszła?

---

## 3. 500 po akceptacji

**Cel:** błąd techniczny nie cofa decyzji biznesowej.

**Gdzie:** LAB 09, LAB 13 negative test.

**Jak odtworzyć:**

1. Przeprowadź Approval do końca.
2. Przed HTTP ustaw Status = `Integration Pending`.
3. Wywołaj API w trybie error:

```bash
curl -s -X PUT "$API/admin/mode" \
  -H 'Content-Type: application/json' \
  -d '{"mode":"error"}'
```

albo `x-mock-mode: 500`, albo numer `VCM/DEMO/500`.

**Oczekiwane:**

- Approval history zostaje,
- Contract = `Integration Error`, nie `Draft` i nie `Rejected`,
- ProcessLog Severity = Error,
- flow kończy się Failed **po** FINALLY.

**Pułapka sali:** Terminate w CATCH. FINALLY się nie wykona.

---

## 4. Race condition / dwa zapisy Status

**Cel:** dwa runy, późniejszy zapis starszego runu.

**Gdzie:** LAB 10, wariant A albo E.

**Przygotowanie:**

1. Wyłącz concurrency control na triggerze albo ustaw Degree of parallelism > 1.
2. Flow po triggerze czeka (`Delay` 2 minuty albo Approval).
3. Potem bez odczytu bieżącego Status robi `Update` na wartość z początku runu.

**Jak odtworzyć:**

1. Umowa `VCM/2026/003`, Status `Submitted`.
2. Run A startuje i wchodzi w Delay/Approval.
3. Ręcznie ustaw Status `Approved` albo uruchom Run B, który zapisuje `Approved`.
4. Run A wraca i zapisuje `Submitted` albo `In Approval`.

**Sygnał:**

> Umowa była Approved, a po kilku minutach wróciła do Submitted.

**Root cause:** stale write. Starszy run nie sprawdził aktualnego stanu.

**Fix:** odczyt rekordu tuż przed update, dozwolone przejścia statusów, concurrency 1, osobny `IntegrationStatus`.

---

## 5. Stale data podczas Approval

**Cel:** dane pobrane przed czekaniem nie są już prawdziwe.

**Gdzie:** LAB 10, wariant D / E.

**Jak odtworzyć:**

1. Flow czyta Amount = 50 000 i idzie tylko w Legal.
2. `Start and wait for an approval`.
3. W trakcie czekania ktoś zmienia Amount na 650 000 w Model-driven App.
4. Flow kończy Legal i ustawia `Approved` bez Finance/Management.

**Root cause:** decyzja na snapshotcie, nie na bieżącym rekordzie.

**Fix:** ponowny Get row przed finalizacją, albo blokada edycji na czas `In Approval`.

---

## 6. Duplicate integration

**Cel:** drugi POST tworzy albo udaje drugi rekord w ERP.

**Gdzie:** LAB 04 challenge, ćwiczenie E02.

**Jak odtworzyć:**

1. Mock w trybie `success`.
2. Uruchom integrację dla `VCM/DEMO/DUP`.
3. Pierwszy POST = 201, zapisz `id`.
4. Ponowne uruchomienie tego samego numeru = 409 i to samo `externalId`.

Jeżeli flow przy 409 ustawia `Integration Error` i retry, pokaż że to zły odruch. 409 ma zapisać istniejące `externalId` i Status `Integrated`.

**Fix:** alternate key / `ExternalSystemId` już wypełnione => skip POST, idempotency key, traktowanie 409 jako sukces biznesowy.

---

## Który wariant kiedy

| Blok | Wariant |
|---|---|
| Dzień 1, po LAB 03 | Trigger loop – tylko pokaz, bez fixu |
| LAB 04 | 429 i 500 |
| LAB 09 | 500 po akceptacji |
| LAB 10 | jeden z: trigger loop, stale write, duplicate |
| LAB 13 demo | 500 na TEST, support email szkoleniowy |

Na jednej umowie rób jedną awarię. Inaczej timeline kłamie.
