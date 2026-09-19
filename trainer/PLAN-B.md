# Plan B – gdy sala nie ma pełnego setupu

Najpierw nazwij blocker. Potem wybierz wariant. Nie mieszaj trzech obejść w jednym flow.

## 1. Akcja HTTP niedostępna (licencja)

Objaw: w designerze nie ma HTTP albo zapis kończy się limitem licencji.

Wariant A – Custom Connector na mock API, jeśli tenant pozwala na custom connectors.

Wariant B – `When an HTTP request is received` + osobny instant flow, który tylko udaje odpowiedź. LAB 04 wtedy ćwiczy Parse JSON i Run after, nie samą akcję HTTP.

Wariant C – Compose z ręcznie wstawionym JSON-em odpowiedzi. Uczestnik przełącza Compose między 201/409/500. To ratuje dzień, ale powiedz wprost, że to atrapa.

Nie obchodź limitu przez prywatne konto uczestnika.

## 2. DLP blokuje HTTP

Objaw: zapis flow kończy się polityką DLP.

Kolejność:

1. sprawdź, czy środowiska szkoleniowe można wyłączyć z polityki albo dostać wyjątek na czas warsztatu,
2. wrzuć HTTP do tej samej grupy co Dataverse,
3. jeżeli nie – Wariant B/C z punktu 1.

Nie proś uczestników o własne konektory spoza tenant.

## 3. Mock API nieosiągalne z chmury

Objaw: `localhost` działa na laptopie prowadzącego, flow dostaje timeout.

Przyczyna: Power Automate nie widzi localhost.

Naprawa:

- wystaw HTTPS (cloudflared, ngrok, Container Apps),
- wpisz publiczny URL do `VCM_API_BASE_URL`,
- sprawdź `curl` spoza sieci prowadzącego.

Awaryjnie: prowadzący odpala API na publicznym hoście i rozdaje jeden URL całej sali.

## 4. Approvals nie dochodzą

Objaw: flow wisi na `Start and wait for an approval`.

Wariant A – ten sam użytkownik zatwierdza we własnym Power Automate -> Approvals.

Wariant B – zamiast Approvals: email z jasną instrukcją i ręczna zmiana `Approval.Status` w Dataverse/SharePoint. Flow czeka na `Status = Approved` pętlą tylko w demie, nie jako wzorzec produkcyjny.

Wariant C – Condition sterowane ręcznym polem `ForcedDecision` na umowie. Użyj wyłącznie gdy Approvals są martwe.

Po powrocie Approvals nie zostawiaj `ForcedDecision` w Solution 1.0.0.0.

## 5. Brak drugiego środowiska

Objaw: jest tylko DEV.

LAB 13 wtedy:

1. export managed i tak zrób – uczy artefaktu,
2. import managed do **tego samego** środowiska tylko jeśli rozumiecie warstwy; lepiej nie,
3. zamiast importu: prowadzący pokazuje własne TEST albo nagranie,
4. uczestnicy wypełniają deployment record i checklistę.

Nie udawaj, że unmanaged w DEV = wdrożenie.

## 6. Uczestnik bez uprawnień Maker

Objaw: nie tworzy tabel albo Solution.

- para z sąsiadem, jedno konto Maker,
- albo worka prowadzącego na rzutniku + uczestnik robi tylko Canvas i testy.

Nie buduj tabel w Default Solution „bo przejdzie”.

## 7. SharePoint Lookup / indeksy niedostępne

Objaw: tenant blokuje tworzenie list albo indeksów.

- prowadzący udostępnia trzy gotowe listy,
- uczestnik i tak przechodzi LAB 02–04,
- w dyskusji i tak nazywamy ograniczenia SharePoint.

## 8. Dataverse nie wstaje w DEV

To jest jedyny blocker, którego nie da się udawać do końca.

Dzień 1 można domknąć na SharePoint. Dnia 2 bez Dataverse nie zaczynaj migracji – przejdź na warsztat teoretyczny modelu, ról i ALM na środowisku prowadzącego.

## 9. Solution Checker / Pipelines niedostępne

Pomiń. LAB 12 i 13 tego nie wymagają. Pipelines są rozszerzeniem na końcu LAB 13.

## 10. Zasada komunikacji

Każde obejście zapisz na tablicy:

```text
Blocker:
Obejście:
Co przez to tracimy:
Czego nadal uczymy:
```

Uczestnik ma wyjść ze świadomością, co było atrapą.
