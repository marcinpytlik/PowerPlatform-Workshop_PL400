# Power Apps + SharePoint Online – przewodnik developerski

## Cel

Ten plik jest indeksem technicznych notatek dla developerów budujących Canvas App na SharePoint Online.

## Dane i model

- [SHAREPOINT-LIMITS-AND-CONSTRAINTS.md](SHAREPOINT-LIMITS-AND-CONSTRAINTS.md)
- [POWERAPPS-SHAREPOINT-FIELD-TYPES.md](POWERAPPS-SHAREPOINT-FIELD-TYPES.md)
- [POWERAPPS-SHAREPOINT-DATA-ACCESS-PATTERNS.md](POWERAPPS-SHAREPOINT-DATA-ACCESS-PATTERNS.md)
- [POWERAPPS-SHAREPOINT-DELEGATION.md](POWERAPPS-SHAREPOINT-DELEGATION.md)
- [POWERAPPS-SHAREPOINT-CONCURRENCY.md](POWERAPPS-SHAREPOINT-CONCURRENCY.md)

## UI i Power Fx

- [POWERAPPS-STATE-AND-VARIABLES.md](POWERAPPS-STATE-AND-VARIABLES.md)
- [POWERAPPS-COMPONENTS-AND-REUSE.md](POWERAPPS-COMPONENTS-AND-REUSE.md)
- [POWERAPPS-RESPONSIVE-AND-ACCESSIBILITY.md](POWERAPPS-RESPONSIVE-AND-ACCESSIBILITY.md)
- [POWERAPPS-NAMING-CONVENTIONS.md](POWERAPPS-NAMING-CONVENTIONS.md)
- [POWERAPPS-CODE-QUALITY.md](POWERAPPS-CODE-QUALITY.md)

## Performance i diagnostyka

- [POWERAPPS-SHAREPOINT-PERFORMANCE.md](POWERAPPS-SHAREPOINT-PERFORMANCE.md)
- [POWERAPPS-SHAREPOINT-DIAGNOSTICS.md](POWERAPPS-SHAREPOINT-DIAGNOSTICS.md)
- [POWERAPPS-ERROR-HANDLING.md](POWERAPPS-ERROR-HANDLING.md)

## Formularze i dokumenty

- [POWERAPPS-SHAREPOINT-FORMS.md](POWERAPPS-SHAREPOINT-FORMS.md)
- [SHAREPOINT-DOCUMENTS-AND-ATTACHMENTS.md](SHAREPOINT-DOCUMENTS-AND-ATTACHMENTS.md)

## Power Automate

- [SHAREPOINT-POWER-AUTOMATE-PATTERNS.md](SHAREPOINT-POWER-AUTOMATE-PATTERNS.md)
- [SHAREPOINT-SECURITY-AND-CONNECTIONS.md](SHAREPOINT-SECURITY-AND-CONNECTIONS.md)

## Testowanie i lifecycle

- [POWERAPPS-TESTING-AND-RELEASE.md](POWERAPPS-TESTING-AND-RELEASE.md)
- [POWERAPPS-SHAREPOINT-ALM.md](POWERAPPS-SHAREPOINT-ALM.md)

## Decyzje architektoniczne

- [WHEN-TO-USE-SPFX-WEBPART.md](WHEN-TO-USE-SPFX-WEBPART.md)
- [WHEN-SHAREPOINT-STOPS-BEING-A-GOOD-BACKEND.md](WHEN-SHAREPOINT-STOPS-BEING-A-GOOD-BACKEND.md)

## Sugerowana kolejność czytania

```text
1. Field Types
2. Delegation
3. Data Access Patterns
4. Performance
5. Error Handling
6. Security and Connections
7. Concurrency
8. State and Variables
9. Code Quality
10. Testing and Release
11. ALM
12. Backend Decision
```

## Główna zasada

Canvas App i SharePoint mogą tworzyć bardzo dobre rozwiązanie, jeżeli:

- model danych pozostaje prosty,
- zapytania są delegowalne,
- security jest projektowane jawnie,
- procesy backendowe mają kontrolowanego właściciela,
- aplikacja jest monitorowana i testowana,
- lifecycle nie zależy od prywatnego konta developera,
- zespół rozpoznaje moment, w którym należy zmienić backend.
