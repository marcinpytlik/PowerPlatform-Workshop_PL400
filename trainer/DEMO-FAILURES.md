# Kontrolowane awarie do demonstracji

## 1. Trigger loop
Flow uruchamia się na modyfikację i sam modyfikuje rekord.

## 2. 429
Mock API zwraca throttling. Uczestnicy analizują retry policy.

## 3. 500
API zwraca błąd po wcześniejszym zatwierdzeniu umowy. Sprawdzamy, czy proces biznesowy pozostaje spójny.

## 4. Race condition
Dwa flowy aktualizują Status tego samego Contract.

## 5. Stale data
Flow pobiera dane, czeka na approval, a w międzyczasie użytkownik zmienia rekord.

## 6. Duplicate integration
Ponowne uruchomienie flow powoduje drugi POST do systemu zewnętrznego.
