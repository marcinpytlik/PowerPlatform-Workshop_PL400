# Vendor Contract Management – wymagania

## Role

- Employee – rejestruje umowę.
- Legal Approver – opiniuje prawnie.
- Finance Approver – zatwierdza finansowo.
- Manager – zatwierdza końcowo.
- Contract Administrator – zarządza procesem.

## Statusy umowy

Status umowy opisuje stan całego procesu biznesowego. Szczegóły poszczególnych akceptacji są przechowywane w rekordach Approval, a nie jako osobne statusy umowy.

- Draft
- Submitted
- In Approval
- Approved
- Rejected
- Integration Pending
- Integrated
- Integration Error

## Reguły przykładowe

1. Umowa powyżej 100 000 wymaga Finance Approval.
2. Umowa powyżej 500 000 wymaga dodatkowo Management Approval.
3. Po pełnej akceptacji dane są wysyłane do zewnętrznego API.
4. Błąd integracji nie może usuwać informacji o wcześniejszych akceptacjach.
5. Każda istotna operacja powinna mieć correlation ID.

W LAB 01–13 flow porównuje **surowe `Amount`**, bez przeliczenia waluty. Progi są kalibrowane do PLN. Rekord `VCM/2026/002` (150 000 EUR) świadomie idzie ścieżką Finance, bo 150 000 > 100 000. Reguła zależna od waluty (EUR > 250 000, Finance Director) to ćwiczenie E01, nie baseline.
