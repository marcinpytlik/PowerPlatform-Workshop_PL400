# Error handling – standard szkoleniowy

## Układ

```text
MAIN FLOW
 |
 +-- Scope TRY
 |     +-- Business Action 1
 |     +-- Business Action 2
 |
 +-- Scope CATCH
 |     +-- Compose error context
 |     +-- Write ProcessLog
 |     +-- Notify support
 |
 +-- Scope FINALLY
       +-- Cleanup / final status
```

## Minimalny kontekst błędu

- FlowName
- FlowRunId
- CorrelationId
- BusinessObjectId
- ActionName
- Timestamp
- HTTP status
- ErrorCode
- Message

## Reguła

Błąd techniczny nie powinien niszczyć prawidłowo zapisanych danych biznesowych.
