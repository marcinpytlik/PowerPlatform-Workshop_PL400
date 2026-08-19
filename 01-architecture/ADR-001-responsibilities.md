# ADR-001 – Podział odpowiedzialności

## Decyzja

- Canvas App odpowiada za UX i walidację interaktywną.
- Dataverse odpowiada za trwały model danych, relacje, bezpieczeństwo i audyt.
- Power Automate odpowiada za orkiestrację procesu.
- Azure Function/API odpowiada za ciężką logikę integracyjną lub transformacje, których nie opłaca się implementować w rozbudowanym flow.
- Model-driven App odpowiada za administrację procesem.

## Antywzorce

- logika całego procesu w jednej formule Power Fx,
- jeden monolityczny flow dla wszystkich przypadków,
- hard-code URL-i i identyfikatorów środowisk,
- przechowywanie relacyjnego modelu w jednej dużej liście SharePoint.
