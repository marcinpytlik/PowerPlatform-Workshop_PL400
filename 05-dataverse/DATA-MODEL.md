# Model Dataverse

## vcm_Supplier

- SupplierId – GUID
- Name – Primary Name
- SupplierCode – Text / Alternate Key
- TaxId – Text
- Country – Text
- Active – Yes/No

## vcm_Contract

- ContractId – GUID
- ContractNumber – Text / Alternate Key
- Supplier – Lookup -> Supplier
- Amount – Currency
- Currency – Choice
- ValidFrom – Date
- ValidTo – Date
- Status – Choice
- Requestor – User/Lookup
- ExternalSystemId – Text
- CorrelationId – Text

## vcm_Approval

- ApprovalId – GUID
- Contract – Lookup -> Contract
- ApprovalType – Choice
- Approver – User/Lookup
- Status – Choice
- DecisionDate – DateTime
- Comment – Multiline

## vcm_ProcessLog

- ProcessLogId – GUID
- Contract – Lookup -> Contract
- FlowName – Text
- FlowRunId – Text
- CorrelationId – Text
- Timestamp – DateTime
- ActionName – Text
- Severity – Choice
- HttpStatus – Whole Number
- ErrorCode – Text
- Message – Multiline

## Relacje

```text
Supplier 1 --- N Contract
Contract 1 --- N Approval
Contract 1 --- N ProcessLog
```
