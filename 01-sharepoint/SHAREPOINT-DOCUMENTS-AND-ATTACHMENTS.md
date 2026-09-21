# SharePoint Online – attachments, biblioteki dokumentów i metadata

## Cel dokumentu

Dokument opisuje wybór pomiędzy attachments elementów listy a biblioteką dokumentów.

## 1. Attachments

Attachments są wygodne dla prostych scenariuszy.

Przykład:

```text
Ticket
  +--> screenshot
  +--> mały PDF
```

## 2. Kiedy attachments wystarczą

- mała liczba plików,
- brak potrzeby niezależnego versioningu,
- brak własnego lifecycle dokumentu,
- dokument jest tylko dodatkiem do rekordu.

## 3. Kiedy używać Document Library

Biblioteka jest lepsza, gdy dokument:

- ma własne metadata,
- ma własny lifecycle,
- podlega wersjonowaniu,
- wymaga approval,
- wymaga retencji,
- ma być wyszukiwany niezależnie,
- jest ważnym obiektem biznesowym.

## 4. Metadata vs foldery

Głębokie foldery zwiększają złożoność ścieżek.

Metadata pozwala klasyfikować dokumenty niezależnie od fizycznej struktury folderów.

## 5. Powiązanie dokumentu z rekordem biznesowym

Typowy model:

```text
Contract
   |
   +--> ContractId / ContractNumber
            |
            v
SharePoint Document Library
```

Dokument może przechowywać metadata identyfikujące powiązany Contract.

## 6. Versioning

Biblioteki dokumentów obsługują pełny versioning plików.

Attachments elementu listy nie powinny być traktowane jako odpowiednik pełnego systemu dokumentowego.

## 7. Search i compliance

Biblioteki lepiej wspierają scenariusze związane z:

- wyszukiwaniem,
- retencją,
- klasyfikacją,
- governance,
- lifecycle dokumentów.

## 8. Anti-pattern

```text
Contract item
+
20 dużych attachments
+
brak metadata
+
brak versioningu
```

Jeżeli dokumenty mają własne znaczenie biznesowe, powinny być modelowane jako dokumenty, a nie tylko attachments.
