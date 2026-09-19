# Troubleshooting flow

## Flow zrobił coś nieprzewidzianego – checklista

1. Znajdź obiekt biznesowy, którego dotyczy incydent.
2. Znajdź FlowRunId lub CorrelationId.
3. Sprawdź trigger inputs.
4. Sprawdź warunki triggera.
5. Sprawdź inputs i outputs każdej istotnej akcji.
6. Sprawdź retry.
7. Sprawdź parallel branches.
8. Sprawdź concurrency control.
9. Sprawdź, czy Update nie uruchomił ponownie triggera.
10. Sprawdź odpowiedź systemu zewnętrznego.
11. Porównaj timestampy wszystkich flowów operujących na tym samym rekordzie.
12. Ustal pierwszy punkt, w którym stan odbiega od oczekiwanego.
