# Skrypt dnia 2 – Dataverse, migracja, Model-driven

**Cel dnia:** ten sam proces działa na Dataverse. SharePoint zostaje punktem odniesienia, nie drugim źródłem prawdy.

**Laby obowiązkowe:** 05, 06, 07.
**LAB 08:** opcjonalny, tylko gdy grupa jedzie zgodnie z planem.
**Design flowów:** rysunek i nazwy, pełna refaktoryzacja zostaje na LAB 12.

## Przygotowanie (08:40)

- Solution jeszcze nie istnieje – uczestnicy utworzą je w LAB 05.
- Przypomnij **jedną** nazwę: `Vendor Contract Management`, prefix `vcm`.
- Nie używaj nazwy `Vendor Contract Management DEV`.

---

## 09:00–10:45 – LAB 05 Dataverse (105 min)

To jest najdłuższy lab warsztatu. Nie skracaj alternate keys i audytu.

Kolejność prowadzenia:

1. 10 min: Publisher + jedno Solution, wersja `0.5.0.0`.
2. 15 min: Choices.
3. 50 min: cztery tabele + relacje + klucze.
4. 15 min: auditing i role.
5. 15 min: dane testowe i tabela porównawcza SharePoint vs Dataverse.

Akcenty:

- Dataverse to nie „lepszy SharePoint”,
- prefix zostaje na zawsze,
- `Process Log` jest append-only.

**Checkpoint:** drugi Supplier z tym samym `Supplier Code` jest blokowany.

---

## 10:45–11:00 – Przerwa

---

## 11:00–12:30 – LAB 06 migracja (90 min)

Najbardziej ryzykowny blok. Ludzie psują działający Canvas.

Zasada: **ekran po ekranie**, stare źródła SharePoint zostają do ostatniego testu.

Prowadzenie:

1. 10 min baseline na SharePoint – zapisać, że działa.
2. 20 min dane testowe do Dataverse.
3. 25 min Canvas: galeria, potem formularze.
4. 25 min nowy flow `VCM - Contract Submitted` na Dataverse.
5. 10 min wyłączenie flow SharePoint i regresja A/B.

Jeżeli ktoś nie dowiezie flow do 12:20: Canvas na Dataverse + trigger Dataverse z jednym Approval. HTTP można podpiąć po lunchu.

**Checkpoint:** nowa umowa z Canvas ląduje w Dataverse, nie na liście SharePoint. Stary flow jest Off.

---

## 12:30–13:00 – Lunch

---

## 13:00–14:00 – LAB 07 Model-driven (60 min)

Cel nie jest „poznać cały App Designer”. Cel: administrator nie potrzebuje 12 ekranów Canvas.

Demo 10 min: subgrid Approvals + Process Logs na formularzu Contract.

Potem uczestnicy: nawigacja, dwa widoki, uruchomienie aplikacji.

Pytanie zamykające:

> Kto jest użytkownikiem Canvas, a kto Model-driven w tym samym Solution?

**Checkpoint:** z Contract widać powiązane Approval i Process Log.

---

## 14:00–14:15 – Bufor / LAB 08

Jeżeli grupa skończyła LAB 07 przed 13:50 i nie ma długów z migracji:

- 30–45 min LAB 08, tylko tytuł, Save i walidacja,
- słownik z `07-multilanguage/translations.csv`.

W przeciwnym razie: LAB 08 jako praca własna. Nie zabieraj czasu ALM-owi.

---

## 14:15–15:15 – Projekt refaktoryzacji flow

Nie implementujemy jeszcze child flows na sali, chyba że ktoś skończył wszystko.

Na tablicy:

```text
VCM - Contract Submitted
   +--> VCM - Approval
   +--> VCM - API Integration
   +--> VCM - Notification
   +--> VCM - Error Handler
```

Omów:

- connection references,
- environment variables `VCM_API_BASE_URL`, `VCM_SUPPORT_EMAIL`,
- dlaczego nie hard-code URL DEV.

Zadanie: każdy rysuje obecny monolit i zaznacza cięcia. Zdjęcia idą do LAB 12.

---

## 15:15–15:30 – Przerwa

---

## 15:30–16:00 – Flow czy kod?

Weź E06: transformacja JSON 40 s, tysiące elementów.

Nie kończ zdaniem „Azure Functions są lepsze”. Kończ kryteriami:

- orkiestracja procesu vs silnik transformacji,
- timeout i limity Power Automate,
- kto utrzymuje kod,
- idempotencja i kontrakt API.

---

## Jeśli dzień się wywróci

| Minimum na 16:00 | Po co |
|---|---|
| Tabele + Solution + Canvas na Dataverse | dzień 3 ma co pakować |
| Nowy trigger Dataverse, choćby z jednym Approval | LAB 09 i 10 mają runy |
| Model-driven z jednym widokiem | deployment ma co otworzyć |

LAB 08 i pełna refaktoryzacja child flows nie są blockerem dnia 3.
