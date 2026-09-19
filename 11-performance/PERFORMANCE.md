# Performance – checklista

## SharePoint

- filtruj u źródła,
- używaj Filter Query,
- indeksuj kolumny filtrujące,
- pobieraj tylko wymagane dane,
- kontroluj pagination,
- unikaj pełnego skanowania dużych list.

## Canvas App

- sprawdzaj delegację,
- ogranicz liczbę requestów,
- unikaj wielokrotnych LookUp dla tych samych danych,
- nie ładuj całej bazy do kolekcji bez potrzeby,
- analizuj Monitor.

## Power Automate

- nie rób Get Items -> Apply to each -> Condition, jeżeli warunek można przesunąć do źródła,
- kontroluj concurrency,
- ogranicz liczbę akcji w pętli,
- używaj retry świadomie,
- obserwuj 429 i limity konektorów.
