# Solution – Vendor Contract Management

## Zasada

Od LAB 05 rozwijamy **jedno docelowe Solution**. Nie tworzymy drugiego Solution przed deploymentem.

## Publisher

- Display name: Vendor Contract Management
- Name: VendorContractManagement
- Prefix: vcm

## Solution

- Display name: Vendor Contract Management
- Name: VendorContractManagement
- DEV: unmanaged
- wersja robocza: 0.5.0.0
- pierwszy artefakt wdrożeniowy: 1.0.0.0

## Komponenty

- Dataverse Tables
- Choices
- Canvas App korzystająca z Dataverse
- Model-driven App
- Cloud Flows / child flows
- Connection References
- Environment Variables

## Docelowy podział flowów

```text
VCM - Contract Submitted
   |
   +--> VCM - Approval
   +--> VCM - API Integration
   +--> VCM - Notification
   +--> VCM - Error Handler / Process Log
```

## Environment Variables

- VCM_API_BASE_URL
- VCM_SUPPORT_EMAIL
- VCM_DEFAULT_CURRENCY
- VCM_ENABLE_EXTERNAL_INTEGRATION

## Connection References

- Dataverse
- Office 365 Outlook
- Approvals
- SharePoint – tylko jeśli po migracji pozostała świadoma zależność
- HTTP / Custom Connector – zależnie od wariantu

## Wersjonowanie

- 1.0.0.0 – baseline
- 1.1.0.0 – funkcjonalność
- 1.1.1.0 – poprawka
- 2.0.0.0 – zmiana wymagająca większej migracji
