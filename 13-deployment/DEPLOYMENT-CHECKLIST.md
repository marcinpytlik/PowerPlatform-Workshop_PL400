# DEV -> TEST -> PROD – checklista

## Przed eksportem

- [ ] wszystkie komponenty znajdują się w Solution
- [ ] Canvas App korzysta z Dataverse, nie ze starego źródła SharePoint
- [ ] produkcyjny flow używa triggera Dataverse
- [ ] stare flow SharePoint jest wyłączone
- [ ] brak hard-code URL i adresów środowiskowych
- [ ] connection references są używane
- [ ] environment variables są zdefiniowane
- [ ] flowy mają właścicieli i poprawne połączenia
- [ ] wykonano test funkcjonalny
- [ ] wykonano test regresyjny po migracji SharePoint -> Dataverse
- [ ] wykonano test błędów
- [ ] sprawdzono zależności Solution
- [ ] ustawiono numer wersji

## TEST

- [ ] import managed solution
- [ ] ustaw wartości environment variables
- [ ] skonfiguruj connection references
- [ ] włącz wymagane flowy
- [ ] wykonaj smoke test
- [ ] wykonaj scenariusz end-to-end
- [ ] sprawdź Process Log

## PROD

- [ ] zaakceptowano wersję z TEST
- [ ] utworzono plan wdrożenia
- [ ] znany jest plan rollback / upgrade
- [ ] wykonano import managed solution
- [ ] skonfigurowano wartości środowiskowe
- [ ] wykonano smoke test
- [ ] zapisano numer wdrożonej wersji
