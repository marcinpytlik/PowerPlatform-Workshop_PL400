# Contract Administration – Model-driven App

Nazwa aplikacji: `VCM - Contract Administration`. Zgodne z LAB 07.

## Navigation

Bez osobnego dashboardu w wariancie 3-dniowym.

- Contracts
- Suppliers
- Approvals
- Process Logs

## Widoki

Budowane w LAB 07:

- `VCM - Active Contracts` – Status != Rejected, sort `Valid To`
- `VCM - Integration Errors` – Status = Integration Error
- `VCM - Errors` na Process Log – Severity = Error lub Critical

Opcjonalne rozszerzenie (nie blocker): Waiting for Approval, Expiring in 30 days.

## Formularz Contract

Sekcje z LAB 07:

1. General – Contract Number, Supplier, Amount, Currency Code, Status
2. Dates – Valid From, Valid To
3. Integration – External System ID, Correlation ID
4. Ownership / requestor – Requestor, Owner

Na formularzu: subgrid Approvals i subgrid Process Logs.
