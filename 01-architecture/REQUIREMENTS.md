# Vendor Contract Management – wymagania

## Role

- Employee – rejestruje umowę.
- Legal Approver – opiniuje prawnie.
- Finance Approver – zatwierdza finansowo.
- Manager – zatwierdza końcowo.
- Contract Administrator – zarządza procesem.

## Statusy umowy

- Draft
- Submitted
- Legal Review
- Financial Review
- Management Approval
- Approved
- Rejected
- Integration Pending
- Integrated
- Error

## Reguły przykładowe

1. Umowa powyżej 100 000 PLN wymaga Finance Approval.
2. Umowa powyżej 500 000 PLN wymaga dodatkowo Management Approval.
3. Po pełnej akceptacji dane są wysyłane do zewnętrznego API.
4. Błąd integracji nie może usuwać informacji o wcześniejszych akceptacjach.
5. Każda istotna operacja powinna mieć correlation ID.
