import pandas as pd
import streamlit as st
from shared.helpers import header_bar, project_nav_box

STATUS_OPTIONS = [
    "-- bitte auswählen --",
    "PM - Produkt Mission",
    "PD - Produkt Definition",
    "PF - Product Feasibility",
    "LH - Lastenheft",
    "Design Freezer",
    "SOP",
    "EOP",
]

VALID_STATUS = set(STATUS_OPTIONS)

def _normalize_status_column():
    """
    Stellt sicher, dass die Projects-Tabelle eine Status-Spalte hat,
    und dass alle Werte gültig sind (sonst -> Placeholder).
    """
    if "Status" not in st.session_state.projects.columns:
        st.session_state.projects["Status"] = "-- bitte auswählen --"

    st.session_state.projects["Status"] = (
        st.session_state.projects["Status"]
        .fillna("-- bitte auswählen --")
        .astype(str)
        .apply(lambda x: x if x in VALID_STATUS else "-- bitte auswählen --")
    )

def _apply_edited_rows_back(edited_view: pd.DataFrame):
    """
    edited_view enthält nur die gefilterten Zeilen (View).
    Wir schreiben Änderungen anhand ProjektNr zurück in st.session_state.projects.
    """
    if edited_view.empty:
        return

    base = st.session_state.projects.copy()
    base = base.set_index("ProjektNr")

    view = edited_view.copy().set_index("ProjektNr")

    # nur Spalten updaten, die im View existieren
    for col in view.columns:
        if col in base.columns:
            base.loc[view.index, col] = view[col]

    st.session_state.projects = base.reset_index()

def render():
    header_bar("Projektübersicht – One-Off Projekte")

    _normalize_status_column()

    left, right = st.columns([0.75, 0.25], gap="large")

    with left:
        df = st.session_state.projects.copy()

        c1, c2 = st.columns([0.6, 0.4])
        with c1:
            q = st.text_input("Projekt suchen (ProjektNr / Kunde / Status)", "")
        with c2:
            status_filter = st.selectbox(
                "Status Filter",
                ["Alle"] + [s for s in STATUS_OPTIONS if s != "-- bitte auswählen --"],
            )

        if q.strip():
            ql = q.strip().lower()
            df = df[df.apply(lambda r: ql in " ".join(map(str, r.values)).lower(), axis=1)]

        if status_filter != "Alle":
            df = df[df["Status"] == status_filter]

        # Reihenfolge wie Screenshot (und Status bleibt Status)
        display_cols = ["ProjektNr", "CPM", "Kunde", "Werksunikat", "Status"]
        df_view = df[display_cols].copy()

        edited_view = st.data_editor(
            df_view,
            use_container_width=True,
            hide_index=True,
            num_rows="fixed",
            column_config={
                "Status": st.column_config.SelectboxColumn(
                    "Status",
                    options=STATUS_OPTIONS,
                    required=False,
                )
            },
            disabled=["ProjektNr", "CPM", "Kunde", "Werksunikat"],  # nur Status editierbar
            key="projects_editor",
        )

        # Änderungen zurückschreiben (nur die gefilterten Zeilen)
        _apply_edited_rows_back(edited_view)

        st.markdown("**Projekt auswählen:**")
        project_options = st.session_state.projects["ProjektNr"].tolist()
        st.session_state.selected_project = st.selectbox(
            "Aktives Projekt",
            options=project_options,
            index=project_options.index(st.session_state.selected_project),
            label_visibility="collapsed",
        )

    with right:
        st.markdown("### Aktionen")

        with st.expander("Neues Projekt anlegen", expanded=False):
            with st.form("new_project"):
                pnr = st.text_input("ProjektNr (z. B. SW-012)")
                cpm = st.text_input("CPM (optional)")
                kunde = st.text_input("Kunde")
                wu = st.text_input("Werksunikat")

                # NEUE Status-Auswahl
                status = st.selectbox("Status", STATUS_OPTIONS, index=0)

                submitted = st.form_submit_button("Projekt speichern")
                if submitted:
                    if not pnr:
                        st.error("Bitte ProjektNr eingeben.")
                    else:
                        new_row = {
                            "ProjektNr": pnr,
                            "CPM": cpm,
                            "Kunde": kunde,
                            "Werksunikat": wu,
                            "Status": status if status in VALID_STATUS else "-- bitte auswählen --",
                        }
                        st.session_state.projects = pd.concat(
                            [st.session_state.projects, pd.DataFrame([new_row])],
                            ignore_index=True,
                        )
                        st.success("Projekt angelegt (Demo).")

        st.button("Projekt bearbeiten", use_container_width=True)
        st.markdown("")
        project_nav_box()
