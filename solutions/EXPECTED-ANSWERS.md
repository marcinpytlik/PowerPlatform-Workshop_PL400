# Oczekiwane kierunki rozwiązań

To nie są jedyne poprawne odpowiedzi. Prowadzący ocenia uzasadnienie, nie zgodność z jednym schematem.

## E01 – Reguła biznesowa (EUR > 250 000)

Dodatkowa akceptacja Finance Director nie powinna żyć wyłącznie w `If` na przycisku Canvas.

Oczekiwany kierunek:

- próg jest zależny od **waluty**, nie od gołego `Amount > 250000`,
- nowy `ApprovalType` (np. Finance Director) albo drugi krok Finance z innym approverem,
- konfiguracja progów w tabeli / Environment Variable, nie w trzech skopiowanych blokach flow,
- Canvas może ostrzec użytkownika, ale decyzja o ścieżce należy do procesu,
- odrzucenie tego kroku kończy proces biznesowo, bez kasowania wcześniejszych Approval.

Antywzorzec: twardy próg w Power Fx i osobny, ręczny mail poza flow.

## E02 – Idempotency

- alternate/external key,
- kontrola ExternalSystemId,
- correlation/request ID,
- API przyjmujące idempotency key, jeżeli wspierane.

W tym warsztacie mock API przy ponownym POST tego samego `contractNumber` zwraca 409 i istniejące `externalId`. Flow powinien potraktować 409 jako znany konflikt biznesowy, nie jako awarię do ślepego retry.

## E03 – Trigger loop

- trigger conditions,
- pole techniczne/status procesu,
- rozdzielenie zdarzeń biznesowych od technicznych aktualizacji,
- dodatkowa kontrola poprzedniego i nowego stanu.

Minimum dwa mechanizmy, nie jeden „i jakoś działa”.

## E04 – Performance (50 000 rekordów)

Ekran ma pokazać **aktywne umowy wybranego dostawcy**, nie całą listę.

Oczekiwany kierunek:

- najpierw wybór Supplier (combo / lookup), potem filtr umów,
- filtr u źródła: dostawca + status, nie `ClearCollect` całej tabeli,
- delegowalna formuła; `StartsWith` / równość zamiast niedelegowalnego `in` na tekście,
- w SharePoint: indeksy i Filter Query; w Dataverse: lookup i widok,
- Monitor do potwierdzenia, że request jest filtrowany.

Antywzorzec: zaciągnięcie 50 000 rekordów do kolekcji i `Filter` po stronie klienta.

## E05 – Error classification

- Business: nie retry automatycznie, czytelny status biznesowy.
- Transient: retry/backoff.
- Technical: log, alert i kontrolowane zakończenie.

409 z mock API to typowo Business. 429 to Transient. 500 to Technical.

## E06 – Architecture

Rozważyć Azure Function lub inną warstwę kodową, szczególnie jeśli flow staje się silnikiem transformacji zamiast orkiestratorem procesu.

Kryteria, nie hasła:

- czas i rozmiar transformacji vs limity Power Automate,
- kto utrzymuje kod,
- czy wynik musi być transakcyjny z zapisem Dataverse,
- czy da się podzielić na orkiestrację + usługę.

## E07 – Security

Same ukrycie przycisku w Canvas nie jest modelem bezpieczeństwa.

Oczekiwany kierunek w Dataverse:

- Employee: Create/Read/Write na własnych umowach (owner = requestor albo team użytkownika),
- Contract Administrator: Organization na Contract, Approval, Process Log,
- Legal: Read (i Write Approval) tylko dla umów w stanie wymagającym Legal Review – przez rolę + widok, access team, albo udział (sharing) nadawany przez flow na czas kroku,
- Process Log: Read dla supportu, nie dla każdego pracownika,
- least privilege; osobne role `VCM Contract User` i `VCM Contract Administrator`.

SharePoint tego wariantu nie dowiezie czysto – to jeden z powodów migracji.

## E08 – Multilanguage (FR bez zmian w kontrolkach)

Kontrolki już biorą tekst z klucza, nie z `If(Language()=...)`.

Oczekiwany kierunek:

- dodać język `fr` do słownika (kolumna albo wiersz),
- dodać `fr` do listy przełącznika i fallbacku,
- nie ruszać formuł `LookUp` / `Switch` w kontrolkach, jeżeli mechanizm jest generyczny,
- jeszcze czystszy wariant: funkcja / komponent biorący tylko `Key`, a zbiór języków siedzi w danych.

Antywzorzec: kopia ekranu FR albo dopisanie `If(varLanguage="fr"; ...)` przy każdej etykiecie.
