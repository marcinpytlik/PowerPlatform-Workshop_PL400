# LAB 12 – Solutions i ALM: pakowanie Vendor Contract Management

## Cel laboratorium

Uporządkować komponenty aplikacji w rozwiązaniu możliwym do kontrolowanego wdrażania między środowiskami.

Po laboratorium uczestnik potrafi:

- utworzyć Publisher,
- utworzyć Solution,
- dodać komponenty,
- używać Connection References,
- używać Environment Variables,
- usunąć hard-code konfiguracji,
- ustawić wersję,
- zrozumieć managed vs unmanaged.

## Czas

90 minut. W agendzie 3-dniowej: **75 min**. Connection references i environment variables są obowiązkowe. Pełny podział na child flows implementuj tylko gdy jest bufor – rysunek z dnia 2 wystarczy jako kierunek.

---

# Zadanie 1 – Weryfikacja Publishera i Solution

W LAB 05 utworzyliśmy docelowego Publishera i jedno Solution. **Nie twórz teraz drugiego rozwiązania.**

Sprawdź:

```text
Publisher: Vendor Contract Management
Prefix: vcm
Solution: Vendor Contract Management
Current version: 0.5.0.0
```

Jeżeli którykolwiek z kluczowych komponentów powstał z innym prefixem, zatrzymaj się i omów konsekwencje. Zmiana publishera później nie zmienia schema names już utworzonych komponentów.

## Dyskusja

Dlaczego nie chcemy przypadkowych prefixów `new_` i komponentów rozrzuconych po Default Solution?

---

# Zadanie 2 – Przygotowanie wersji 1.0.0.0

Otwórz istniejące Solution `Vendor Contract Management`.

W środowisku DEV pozostaje ono **unmanaged**. Przed pierwszym eksportem ustawimy wersję:

```text
1.0.0.0
```

---

# Zadanie 3 – Dodanie tabel Dataverse

Dodaj istniejące:

- Supplier,
- Contract,
- Approval,
- Process Log.

Przy dodawaniu istniejących tabel sprawdź, czy wymagane komponenty zależne również trafiają do Solution:

- columns,
- relationships,
- forms,
- views,
- choices.

Nie dodawaj automatycznie wszystkiego bez refleksji; uczymy się świadomie kontrolować zależności.

---

# Zadanie 4 – Dodanie aplikacji

Dodaj:

```text
VCM - Contract Portal
VCM - Contract Administration
```

Jeżeli Canvas App była pierwotnie utworzona poza Solution, dodaj ją do rozwiązania i sprawdź zależności.

---

# Zadanie 5 – Refaktoryzacja i dodanie flowów

Po migracji z LAB 06 uporządkuj proces przed wdrożeniem. Jeśli nadal istnieje jeden monolityczny flow, rozdziel odpowiedzialności na solution-aware cloud flows/child flows tam, gdzie ma to sens.

Docelowe nazwy:

```text
VCM - Contract Submitted
VCM - Approval
VCM - API Integration
VCM - Notification
VCM - Error Handler
```

Minimalny docelowy układ:

```text
VCM - Contract Submitted (orchestrator)
   |
   +--> VCM - Approval
   +--> VCM - API Integration
   +--> VCM - Notification
   +--> VCM - Error Handler / Process Log
```

Jeżeli ograniczenia środowiska uniemożliwiają child flows, zachowaj podział odpowiedzialności w osobnych solution-aware flows i udokumentuj sposób ich wywołania.

---

# Zadanie 6 – Connection References

Dla każdego solution-aware flow sprawdź połączenia.

Utwórz lub wybierz Connection References dla:

- Dataverse,
- SharePoint – jeśli nadal używany,
- Office 365 Outlook,
- Approvals,
- innych connectorów wymaganych w środowisku.

Nazewnictwo:

```text
VCM - Dataverse
VCM - SharePoint
VCM - Outlook
VCM - Approvals
```

## Dlaczego?

Flow nie powinien być na stałe związany z konkretnym połączeniem z DEV. Podczas importu rozwiązania do TEST connection reference zostaje powiązany z właściwym connection target environment.

---

# Zadanie 7 – Environment Variables

Utwórz:

```text
VCM_API_BASE_URL
VCM_SUPPORT_EMAIL
VCM_DEFAULT_CURRENCY
VCM_ENABLE_EXTERNAL_INTEGRATION
```

Typy:

- API URL – Text,
- Support Email – Text,
- Default Currency – Text,
- Enable Integration – Yes/No lub Text/JSON zależnie od standardu organizacji.

## Default value vs Current value

Omów:

- wartość domyślna jest częścią definicji,
- current value jest wartością środowiskową,
- podczas deploymentu target może otrzymać inną wartość.

Przykład:

```text
DEV  -> https://api-dev.example/...
TEST -> https://api-test.example/...
PROD -> https://api.example/...
```

---

# Zadanie 8 – Usunięcie hard-code

Znajdź w flow:

```text
https://api-dev...
```

Zastąp Environment Variable `VCM_API_BASE_URL`.

Znajdź adres supportu wpisany literalnie i zastąp `VCM_SUPPORT_EMAIL`.

Znajdź domyślną walutę i oceń, czy powinna być:

- Environment Variable,
- Choice,
- dane biznesowe.

Nie wszystko jest configuration.

---

# Zadanie 9 – Solution Checker / kontrola jakości

Jeżeli Solution Checker jest dostępny:

1. uruchom kontrolę,
2. przejrzyj warnings/errors,
3. sklasyfikuj:
   - must fix,
   - accepted risk,
   - not applicable.

Nie ignoruj ostrzeżeń automatycznie, ale też nie traktuj każdego warningu jak awarii produkcyjnej.

---

# Zadanie 10 – Dependencies

Użyj **Show dependencies / Advanced -> dependencies** w zakresie dostępnego UI.

Sprawdź dla:

- Contract table,
- Canvas App,
- flow integracyjnego.

Zapisz minimum trzy zależności.

---

# Zadanie 11 – Wersjonowanie

Ustal regułę szkoleniową:

```text
1.0.0.0 baseline
1.1.0.0 nowa funkcjonalność
1.1.1.0 poprawka
2.0.0.0 większa zmiana/migracja
```

Ustaw:

```text
1.0.0.0
```

przed pierwszym eksportem.

---

# Zadanie 12 – Managed vs unmanaged

W grupach odpowiedz:

## DEV

```text
Unmanaged
```

Dlaczego? Tu rozwijamy i edytujemy komponenty.

## TEST/PROD

Docelowy wzorzec:

```text
Managed
```

Omów solution layers i ryzyko ręcznych zmian na produkcji.

---

# Test końcowy

Sprawdź zawartość Solution:

```text
Vendor Contract Management 1.0.0.0
|
+-- Tables
+-- Choices
+-- Canvas App
+-- Model-driven App
+-- Cloud Flows
+-- Connection References
+-- Environment Variables
```

Uruchom aplikacje i flow w DEV po usunięciu hard-code.

Jeśli proces działa wyłącznie dlatego, że wartość jest jeszcze wpisana literalnie w akcji, LAB nie jest ukończony.

---

# Kryterium ukończenia

- wszystkie kluczowe komponenty znajdują się w Solution,
- używane są connection references,
- URL i support email są environment variables,
- wersja = 1.0.0.0,
- flow działa po refaktoryzacji konfiguracji.

---

# Materiał Microsoft

- Environment variables: https://learn.microsoft.com/en-us/power-apps/maker/data-platform/environmentvariables
- Connection references: https://learn.microsoft.com/en-us/power-apps/maker/data-platform/create-connection-reference
- Import/export solutions: https://learn.microsoft.com/en-us/power-apps/maker/data-platform/import-update-export-solutions
