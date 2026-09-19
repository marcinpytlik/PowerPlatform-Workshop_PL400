# Setup szkolenia – Power Platform Advanced Workshop

Ten dokument jest listą kontrolną **przed dniem 1**. Bez domkniętego setupu LAB 04, 09, 12 i 13 będą gaszeniem pożarów, a nie szkoleniem.

## Cel setupu

Po przygotowaniu uczestnik i prowadzący mają:

- dwa środowiska Power Platform z Dataverse,
- witrynę SharePoint na prototyp,
- działające Approvals,
- dozwoloną akcję HTTP albo jawny plan B,
- uruchomione mock API z trybami 201 / 409 / 429 / 500,
- konta testowe o znanych rolach.

---

# 1. Tenant i licencje

## Tenant

- jeden tenant szkoleniowy, nie produkcyjny,
- prowadzący jest Environment Admin albo ma osobę z takimi uprawnieniami na miejscu,
- uczestnicy logują się kontami szkoleniowymi, nie prywatnymi.

## Licencje – minimum

Na konto **uczestnika** i **prowadzącego**:

| Składnik | Potrzebne do | Uwagi |
|---|---|---|
| Power Apps | Canvas App, Model-driven App | Per User albo środowisko deweloperskie |
| Power Automate | cloud flows, Approvals | Per User albo w pakiecie Power Apps |
| Dataverse | LAB 05–13 | środowisko Developer / Trial / Sandbox |
| Premium / HTTP | LAB 04, 09, 13 | akcja HTTP jest premium |
| Exchange / Outlook | powiadomienia | skrzynka musi przyjmować mail |
| Teams – opcjonalnie | powiadomienia techniczne | nie jest blocker |

## Sprawdzenie licencji

1. `https://admin.powerplatform.microsoft.com`
2. Użytkownicy -> wybrane konto szkoleniowe.
3. Potwierdź Power Apps i Power Automate.
4. W Power Automate utwórz pusty instant flow i sprawdź, czy akcja **HTTP** jest widoczna.

Jeżeli HTTP jest zablokowane licencją albo DLP, od razu przygotuj [plan B](trainer/PLAN-B.md).

---

# 2. Środowiska

Potrzebne są **dwa** środowiska. LAB 13 bez drugiego środowiska nie ma sensu.

| Środowisko | Przeznaczenie | Dataverse | Solution |
|---|---|---|---|
| `VCM-DEV` | budowa, unmanaged | tak | `Vendor Contract Management` |
| `VCM-TEST` | import managed, smoke test | tak | to samo Solution, managed |

Nazwy mogą być inne, ale muszą być **jednoznaczne**. Nie używaj `Default` jako TEST.

## Tworzenie

1. Power Platform Admin Center -> Environments -> New.
2. Type: Sandbox albo Developer.
3. Dataverse: Yes.
4. Region: ta sama dla DEV i TEST.
5. Security group: tylko konta szkoleniowe.

## Uprawnienia

| Rola | DEV | TEST |
|---|---|---|
| Prowadzący | System Administrator | System Administrator |
| Uczestnik | Environment Maker + System Customizer albo równoważne | Basic User + role VCM z LAB 05 po imporcie |
| Konta approverów | dostęp do Dataverse i Approvals | dostęp do Dataverse i Approvals |

W DEV uczestnik musi móc tworzyć tabele, aplikacje, flowy i Solution. W TEST wystarczy uruchamiać aplikacje i zatwierdzać, jeśli deployment robi prowadzący.

## Check

- [ ] oba środowiska istnieją i mają Dataverse,
- [ ] uczestnik widzi `VCM-DEV` na `make.powerapps.com`,
- [ ] prowadzący potrafi przełączyć się na `VCM-TEST`,
- [ ] nazwa środowiska jest widoczna w nagłówku – omów to w dniu 3.

---

# 3. DLP

DLP rozstrzyga, czy LAB 04 w ogóle wystartuje.

## Zasada szkoleniowa

W środowiskach warsztatowych:

- SharePoint, Dataverse, Approvals, Office 365 Outlook – **Business**,
- HTTP / HTTP with Azure AD – **Business** albo osobna polityka szkoleniowa, która ich nie blokuje,
- nie mieszaj konektorów Business i Non-business w jednym flow, jeśli polityka to rozdziela.

## Check

1. Admin Center -> Data policies.
2. Sprawdź, która polityka obejmuje `VCM-DEV` i `VCM-TEST`.
3. Utwórz flow z Dataverse + HTTP.
4. Zapisz. Jeżeli zapis kończy się błędem DLP, nie idź dalej „na żywioł”.

Jeżeli tenant produkcyjny nie pozwala poluzować DLP:

- postaw mock API za Custom Connector w dozwolonej grupie, albo
- użyj wariantu z [PLAN-B](trainer/PLAN-B.md).

Nie obchodź DLP organizacji przez prywatne konektory uczestników.

---

# 4. Approvals

LAB 03, 06, 10 i 13 używają `Start and wait for an approval`.

## Przygotowanie

1. Na koncie prowadzącego i jednym koncie approvera otwórz Power Automate -> Approvals.
2. Uruchom jednorazowo pusty approval testowy, aby provisioning przeszedł przed salą.
3. Sprawdź, czy mail/Teams z approval dochodzi.
4. Potwierdź, że skrzynki nie są pełne i nie lądują w kwarantannie.

## Ograniczenia

- ten sam użytkownik może być requestorem i approverem w środowisku szkoleniowym,
- w większej grupie przygotuj 2–3 skrzynki współdzielone albo aliasy,
- nie używaj prywatnych skrzynek produkcyjnych.

## Check

- [ ] testowy approval kończy się Approve i Reject,
- [ ] mail dochodzi w mniej niż 2 minuty,
- [ ] jest plan B: ręczna zmiana statusu w Dataverse / SharePoint.

---

# 5. HTTP i mock API

## Endpoint

Repozytorium zawiera mock API:

- kod: [`mock-api/`](mock-api/README.md),
- kontrakt: [`11-api-integration/openapi.yaml`](11-api-integration/openapi.yaml).

Tryby:

| Tryb | HTTP | Po co |
|---|---:|---|
| `success` | 201 | happy path, zapis `ExternalSystemId` |
| `conflict` | 409 | błąd biznesowy, bez ślepego retry |
| `throttle` | 429 | retry policy i `Retry-After` |
| `error` | 500 | CATCH, ProcessLog, `Integration Error` |
| `timeout` | brak odpowiedzi w czasie PT30S | Timed out |

## Uruchomienie prowadzącego

Najprostszy wariant na sali:

```bash
cd mock-api
python3 server.py
```

Domyślnie nasłuchuje na `0.0.0.0:8080`. Publiczny URL (ngrok, cloudflared, Container Apps, Azure Function) wpisz do Environment Variable `VCM_API_BASE_URL`.

## Check

```bash
curl -s http://localhost:8080/health
curl -s -X POST http://localhost:8080/api/contracts \
  -H 'Content-Type: application/json' \
  -d '{"contractNumber":"VCM/2026/001","supplierCode":"SUP-001","amount":50000,"currency":"PLN","correlationId":"demo"}'
```

Oczekiwane: `201` oraz `id` w formacie `ERP-...`.

Szczegóły trybów: [`mock-api/README.md`](mock-api/README.md).

---

# 6. SharePoint

## Witryna

Jedna witryna na grupę albo jedna na uczestnika, jeśli tenant na to pozwala.

Przykład:

```text
https://<tenant>.sharepoint.com/sites/PowerPlatformWorkshop
```

Uprawnienia uczestnika: Edit albo Full Control na tej witrynie. Bez tego nie utworzą list i indeksów.

## Check

- [ ] uczestnik tworzy pustą listę,
- [ ] uczestnik dodaje kolumnę Lookup,
- [ ] witryna jest w tym samym tenancie co Power Apps.

Nie używaj OneDrive jako substytutu witryny szkoleniowej.

---

# 7. Konta testowe

Przygotuj minimum cztery tożsamości. Mogą to być osobne konta albo aliasy, ale adresy muszą być znane przed salą.

| Alias | Rola | Użycie |
|---|---|---|
| `vcm-employee` | Employee | Canvas App, Requestor |
| `vcm-legal` | Legal Approver | Approval Legal |
| `vcm-finance` | Finance Approver | Approval Finance |
| `vcm-admin` | Contract Administrator / prowadzący | Model-driven, deployment, mock API |

W małej grupie prowadzący może pełnić Finance i Legal. Zapisz to na tablicy, żeby nikt nie czekał na mail do nieistniejącej skrzynki.

## Dane, które rozdajesz na starcie

```text
Środowisko DEV:
Środowisko TEST:
Witryna SharePoint:
Mock API base URL:
Employee:
Legal:
Finance:
Support email szkoleniowy:
```

Support email **nie może** być produkcyjną skrzynką SOC.

---

# 8. Solution i nazewnictwo

Od LAB 05 wszyscy pracują na **jednym** Solution:

```text
Publisher display name: Vendor Contract Management
Publisher name:         VendorContractManagement
Prefix:                 vcm
Solution display name:  Vendor Contract Management
Solution name:          VendorContractManagement
```

Nie twórz `Vendor Contract Management DEV`. DEV to środowisko, nie nazwa Solution.

---

# 9. Checklist dzień przed szkoleniem

Prowadzący:

- [ ] DEV i TEST żyją, Dataverse odpowiada,
- [ ] DLP nie blokuje HTTP albo jest uzgodniony plan B,
- [ ] Approvals przechodzą test Approve/Reject,
- [ ] mock API odpowiada 201 / 409 / 429 / 500 / timeout,
- [ ] publiczny URL API jest stały na 3 dni,
- [ ] konta testowe logują się na `make.powerapps.com`,
- [ ] witryna SharePoint jest pusta albo ma uzgodniony prefix list,
- [ ] uczestnicy dostali wymagania sprzętowe: przeglądarka Edge/Chrome, drugi monitor mile widziany,
- [ ] wydrukowana albo otwarta [agenda](00-agenda/AGENDA.md) i [skrypt dnia 1](trainer/SCRIPT-DAY-1.md).

Uczestnik:

- [ ] loguje się do DEV,
- [ ] widzi Power Apps, Power Automate, SharePoint,
- [ ] nie ma MFA-blokera na sali (telefon, TAP, skip).

---

# 10. Checklist poranek dnia 1

- [ ] mock API health = OK,
- [ ] próbny flow HTTP z DEV kończy się 201,
- [ ] Approval testowy dochodzi,
- [ ] na tablicy są URL-e i aliasy,
- [ ] uczestnicy są w `VCM-DEV`, nie w Default.

Jeżeli którykolwiek punkt pada, nie zaczynaj LAB 01 „bo się rozkręci”. Najpierw [PLAN-B](trainer/PLAN-B.md).
