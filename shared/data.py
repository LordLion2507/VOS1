from datetime import date
import pandas as pd

def seed_data():
    projects = pd.DataFrame(
        [
            {"ProjektNr": "SW-001", "CPM": "CPM-1001", "Kunde": "Kunde A", "Werksunikat": "WU-01", "Status": "Open"},
            {"ProjektNr": "SW-002", "CPM": "CPM-1002", "Kunde": "Kunde B", "Werksunikat": "WU-02", "Status": "In Progress"},
            {"ProjektNr": "SW-003", "CPM": "CPM-1003", "Kunde": "Kunde C", "Werksunikat": "WU-03", "Status": "Planned"},
            {"ProjektNr": "SW-004", "CPM": "CPM-1004", "Kunde": "Kunde D", "Werksunikat": "WU-04", "Status": "Open"},
            {"ProjektNr": "SW-005", "CPM": "CPM-1005", "Kunde": "Kunde E", "Werksunikat": "WU-05", "Status": "Done"},
        ]
    )

    change_list = pd.DataFrame(
        [
            {
                "ProjektNr": "SW-001",
                "Option": "OE3-001",
                "CPM Unterpunkt (+U?)": "—",
                "KFMAG": "—",
                "Beschreibung (Sonderwunsch/Baugruppe)": "Allgemeines/ Gesamtfahrzeug",
                "Beispielbild": "—",
                "Teilenummer": "—",
                "Kategorie": "Neuentwicklung",
                "Regulatory evaluation": "—",
                "DTV + Abteilung / PE": "—",
                "K-Freigabe": "Freigabe intern",
                "Qualität Norm + Abteilung": "—",
                "Bemusterung": "Ja",
                "HAL-Unterschrift": "—",
                "QC Ersatzteil-Vorlauf": "—",
                "Bemerkungen": "",
                "Wann zuletzt geändert": "2026-01-20",
            },
            {
                "ProjektNr": "SW-001",
                "Option": "OE3-002",
                "CPM Unterpunkt (+U?)": "—",
                "KFMAG": "—",
                "Beschreibung (Sonderwunsch/Baugruppe)": "Konstruktion",
                "Beispielbild": "—",
                "Teilenummer": "—",
                "Kategorie": "—",
                "Regulatory evaluation": "—",
                "DTV + Abteilung / PE": "—",
                "K-Freigabe": "—",
                "Qualität Norm + Abteilung": "—",
                "Bemusterung": "Ja",
                "HAL-Unterschrift": "—",
                "QC Ersatzteil-Vorlauf": "—",
                "Bemerkungen": "",
                "Wann zuletzt geändert": "2026-01-22",
            },
            {
                "ProjektNr": "SW-001",
                "Option": "OE3-003",
                "CPM Unterpunkt (+U?)": "—",
                "KFMAG": "—",
                "Beschreibung (Sonderwunsch/Baugruppe)": "Zulassung, Gesetze und Normen",
                "Beispielbild": "—",
                "Teilenummer": "—",
                "Kategorie": "—",
                "Regulatory evaluation": "—",
                "DTV + Abteilung / PE": "—",
                "K-Freigabe": "—",
                "Qualität Norm + Abteilung": "—",
                "Bemusterung": "Ja",
                "HAL-Unterschrift": "—",
                "QC Ersatzteil-Vorlauf": "—",
                "Bemerkungen": "",
                "Wann zuletzt geändert": "2026-01-18",
            },
            {
                "ProjektNr": "SW-001",
                "Option": "OE3-004",
                "CPM Unterpunkt (+U?)": "—",
                "KFMAG": "—",
                "Beschreibung (Sonderwunsch/Baugruppe)": "Aerodynamik",
                "Beispielbild": "—",
                "Teilenummer": "—",
                "Kategorie": "—",
                "Regulatory evaluation": "—",
                "DTV + Abteilung / PE": "—",
                "K-Freigabe": "—",
                "Qualität Norm + Abteilung": "—",
                "Bemusterung": "Ja",
                "HAL-Unterschrift": "—",
                "QC Ersatzteil-Vorlauf": "—",
                "Bemerkungen": "",
                "Wann zuletzt geändert": "2026-01-14",
            },
            {
                "ProjektNr": "SW-001",
                "Option": "OE3-005",
                "CPM Unterpunkt (+U?)": "—",
                "KFMAG": "—",
                "Beschreibung (Sonderwunsch/Baugruppe)": "Fahrzeugsicherheit",
                "Beispielbild": "—",
                "Teilenummer": "—",
                "Kategorie": "—",
                "Regulatory evaluation": "—",
                "DTV + Abteilung / PE": "—",
                "K-Freigabe": "Freigabe",
                "Qualität Norm + Abteilung": "—",
                "Bemusterung": "Ja",
                "HAL-Unterschrift": "—",
                "QC Ersatzteil-Vorlauf": "—",
                "Bemerkungen": "",
                "Wann zuletzt geändert": "2026-01-12",
            },
            {
                "ProjektNr": "SW-001",
                "Option": "OE3-006",
                "CPM Unterpunkt (+U?)": "—",
                "KFMAG": "—",
                "Beschreibung (Sonderwunsch/Baugruppe)": "Leichtbau",
                "Beispielbild": "—",
                "Teilenummer": "—",
                "Kategorie": "—",
                "Regulatory evaluation": "—",
                "DTV + Abteilung / PE": "—",
                "K-Freigabe": "—",
                "Qualität Norm + Abteilung": "—",
                "Bemusterung": "Ja",
                "HAL-Unterschrift": "—",
                "QC Ersatzteil-Vorlauf": "—",
                "Bemerkungen": "",
                "Wann zuletzt geändert": "2026-01-11",
            },
            {
                "ProjektNr": "SW-001",
                "Option": "OE3-007",
                "CPM Unterpunkt (+U?)": "—",
                "KFMAG": "—",
                "Beschreibung (Sonderwunsch/Baugruppe)": "Elektrik und Elektronik",
                "Beispielbild": "—",
                "Teilenummer": "—",
                "Kategorie": "Neuentwicklung",
                "Regulatory evaluation": "—",
                "DTV + Abteilung / PE": "—",
                "K-Freigabe": "Episode",
                "Qualität Norm + Abteilung": "—",
                "Bemusterung": "Ja",
                "HAL-Unterschrift": "—",
                "QC Ersatzteil-Vorlauf": "—",
                "Bemerkungen": "",
                "Wann zuletzt geändert": "2026-01-10",
            },
        ]
    )

    topics = pd.DataFrame(
        [
            {
                "ProjektNr": "SW-001",
                "ThemenblattID": "TB-014",
                "Titel": "Sonderstreifen – Spezifikation und Umsetzung",
                "Status": "In Bearbeitung",
                "Owner": "Du",
                "LetzteÄnderung": "2026-01-26",
                "Beschreibung": (
                    "Im Rahmen des One-Off Projekts soll ein Sonderstreifen gemäß Kundenanforderung umgesetzt werden. "
                    "Der Sonderstreifen weicht in Farbe, Materialausführung und Positionierung vom Serienstandard ab "
                    "und muss designseitig sowie fertigungstechnisch geprüft und freigegeben werden.\n\n"
                    "Ziel dieses Themenblatts ist die Bündelung aller relevanten Informationen zur Spezifikation, Abstimmung und Umsetzung.\n\n"
                    "Aktueller Stand:\n- Kundenanforderung liegt vor\n- Machbarkeitsprüfung positiv\n- Kostenabschätzung in Arbeit\n\n"
                    "Offene Punkte:\n- Farb-Muster vom Kunden\n- Zeichnungsfreigabe\n- Entscheidung Fertigungsmethode (Lack/Folie)"
                ),
            },
            {"ProjektNr": "SW-001", "ThemenblattID": "TB-002", "Titel": "Kostenanalyse", "Status": "Open", "Owner": "Du", "LetzteÄnderung": "2026-01-23", "Beschreibung": "Kostenanalyse und Budgetabweichungen."},
            {"ProjektNr": "SW-001", "ThemenblattID": "TB-005", "Titel": "Risikomanagement", "Status": "Open", "Owner": "Max", "LetzteÄnderung": "2026-01-19", "Beschreibung": "Risiken und Maßnahmen."},
            {"ProjektNr": "SW-002", "ThemenblattID": "TB-007", "Titel": "Qualitätskontrolle", "Status": "Done", "Owner": "Du", "LetzteÄnderung": "2026-01-15", "Beschreibung": "Qualitätsprüfungen und Nachweise."},
        ]
    )

    lop = pd.DataFrame(
        [
            {
                "Arbeitsaufgabe": "Termin Einkauf",
                "Beschreibung": "Abstimmung Lieferant & Konditionen",
                "Kategorie": "Einkauf",
                "Status": "Open",
                "Priorität": "Hoch",
                "Startdatum": "2026-01-18",
                "Fälligkeitsdatum": "2026-01-28",
                "Zugewiesen an": "Du",
                "Notizen": "Terminvorschläge senden",
                "Wichtige Projekte": "SW-001",
                "+ Spalte hinzufügen": "",
            },
            {
                "Arbeitsaufgabe": "Kostenpositionen",
                "Beschreibung": "PAG-Blöcke abstimmen",
                "Kategorie": "Kalkulation",
                "Status": "In Progress",
                "Priorität": "Mittel",
                "Startdatum": "2026-01-20",
                "Fälligkeitsdatum": "2026-02-05",
                "Zugewiesen an": "Max",
                "Notizen": "Offene Punkte sammeln",
                "Wichtige Projekte": "SW-001",
                "+ Spalte hinzufügen": "",
            },
            {
                "Arbeitsaufgabe": "Dokumente sammeln",
                "Beschreibung": "Unterlagen für Kundenfreigabe",
                "Kategorie": "PM",
                "Status": "Planned",
                "Priorität": "Mittel",
                "Startdatum": "2026-01-25",
                "Fälligkeitsdatum": "2026-02-10",
                "Zugewiesen an": "Du",
                "Notizen": "Ordnerstruktur prüfen",
                "Wichtige Projekte": "SW-002",
                "+ Spalte hinzufügen": "",
            },
        ]
    )

    drive_tree = {
        "0 - Projektmanagement": {},
        "1 - Vertrag und Rechnungen": {},
        "2 - Kundensteckbrief": {},
        "3 - Steckbrief und Visualisierungen": {},
        "4 - Fahrzeuginfos": {},
        "5 - Präsentationen": {},
        "6 - Technik": {},
        "7 - Kundentermine": {},
        "8 - Marketing inkl_IDG_Bilder": {},
        "z_Archiv": {},
    }

    return projects, change_list, topics, lop, drive_tree
