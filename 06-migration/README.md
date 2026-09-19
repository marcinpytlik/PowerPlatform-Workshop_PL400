# Migracja SharePoint → Dataverse

Moduł odpowiada **LAB 06**. Nie budujemy tu drugiego modelu danych – przenosimy działający prototyp z LAB 01–04 na tabele z LAB 05.

## Stan przed

```text
Canvas App → SharePoint → Power Automate (VCM - Contract Submitted - SP)
```

Model: [`../01-sharepoint/DATA-MODEL.md`](../01-sharepoint/DATA-MODEL.md).

## Stan po

```text
Canvas App → Dataverse → Power Automate (VCM - Contract Submitted)
```

Model: [`../05-dataverse/DATA-MODEL.md`](../05-dataverse/DATA-MODEL.md).

SharePoint zostaje punktem odniesienia. Stary flow jest wyłączony, nie usuwany.

## Instrukcja

Krok po kroku: [`../labs/LAB-06-sharepoint-to-dataverse.md`](../labs/LAB-06-sharepoint-to-dataverse.md).

Wzorzec: **Strangler Migration** – [`../00-architecture/POWER-PLATFORM-PATTERNS.md`](../00-architecture/POWER-PLATFORM-PATTERNS.md). Na sali: [`../trainer/THEORY-TALK-TRACK.md`](../trainer/THEORY-TALK-TRACK.md).
