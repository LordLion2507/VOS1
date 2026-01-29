import pandas as pd
import streamlit as st
from shared.helpers import header_bar

def render():
    header_bar("Kalkulationsvorlage")

    # Erste Spalte ist jetzt "Typ" (für Soll / Ist / weitere Zeilen)
    base_cols = [
        "Typ",
        "PAG Kostenblöcke",
        "Anzahl Fahrzeuge",
        "Invest (Werkzeuge)",
        "MEK (Teile Kunden Fahrzeuge) Nicht COP-A",
        "MEK COP-A inkl. Marge",
        "PT-Mat",
        "Eigen-E",
        "Fremd-E",
        "Gewerbliche Stunden",
        "Qualität, Bemusterung",
        "Prüfkosten, Versuchsträger",
        "Equipment, Anlagen, Prüfstände",
        "Zertifizierung, Zulassung",
        "Fahrzeugdokumentation",
        "Marketing und Kundenbegeisterung",
        "FTE indirekt (PAG)",
        "Eingabe (leer)",
    ]

    # Init: 2 Zeilen fix für Soll/Ist
    if "costing_df" not in st.session_state:
        st.session_state.costing_df = pd.DataFrame(
            [
                {c: "" for c in base_cols},  # Soll
                {c: "" for c in base_cols},  # Ist
            ],
            columns=base_cols,
        )

        st.session_state.costing_df.loc[0, "Typ"] = "Soll"
        st.session_state.costing_df.loc[1, "Typ"] = "Ist"

        # Optional: Beispielwerte
        st.session_state.costing_df.loc[0, "PAG Kostenblöcke"] = "One-Off"
        st.session_state.costing_df.loc[0, "Anzahl Fahrzeuge"] = 1
        st.session_state.costing_df.loc[1, "PAG Kostenblöcke"] = "One-Off"
        st.session_state.costing_df.loc[1, "Anzahl Fahrzeuge"] = 1

    # Falls später mal jemand die Soll/Ist Zeilen löscht: wiederherstellen
    df = st.session_state.costing_df.copy()

    if df.shape[0] < 2:
        # auffüllen auf min 2 rows
        while df.shape[0] < 2:
            df = pd.concat([df, pd.DataFrame([{c: "" for c in base_cols}])], ignore_index=True)

    # Typ-Spalte sicher setzen
    df.loc[0, "Typ"] = "Soll"
    df.loc[1, "Typ"] = "Ist"

    edited = st.data_editor(
        df,
        use_container_width=True,
        num_rows="dynamic",
        hide_index=True,
        column_config={
            "Typ": st.column_config.TextColumn(""),  # Header bewusst leer, wie du es wolltest
        },
        disabled=["Typ"],  # Soll/Ist Labels nicht überschreibbar
    )

    # Nach Edit sicherstellen, dass Soll/Ist weiterhin korrekt drinstehen
    if edited.shape[0] >= 2:
        edited.loc[0, "Typ"] = "Soll"
        edited.loc[1, "Typ"] = "Ist"

    st.session_state.costing_df = edited
