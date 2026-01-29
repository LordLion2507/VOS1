import streamlit as st
import pandas as pd
from datetime import date

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Sonderwunsch – One-Off Projekte",
    page_icon="🧩",
    layout="wide"
)

# -----------------------------
# Dummy data (lokal, nur Demo)
# -----------------------------
def seed_data():
    projects = pd.DataFrame([
        {"ProjektNr": "SW-001", "CPM": "CPM-1001", "Kunde": "Kunde A", "Werksunikat": "WU-01", "Status": "Open"},
        {"ProjektNr": "SW-002", "CPM": "CPM-1002", "Kunde": "Kunde B", "Werksunikat": "WU-02", "Status": "In Progress"},
        {"ProjektNr": "SW-003", "CPM": "CPM-1003", "Kunde": "Kunde C", "Werksunikat": "WU-03", "Status": "Planned"},
        {"ProjektNr": "SW-004", "CPM": "CPM-1004", "Kunde": "Kunde D", "Werksunikat": "WU-04", "Status": "Open"},
        {"ProjektNr": "SW-005", "CPM": "CPM-1005", "Kunde": "Kunde E", "Werksunikat": "WU-05", "Status": "Done"},
    ])

    change_list = pd.DataFrame([
        {"ProjektNr": "SW-001", "ÄnderungsID": "A-001", "Kurzbeschreibung": "Bauteil anpassen", "Status": "Open", "Wann zuletzt geändert": "2026-01-20"},
        {"ProjektNr": "SW-001", "ÄnderungsID": "A-002", "Kurzbeschreibung": "Schnittstelle prüfen", "Status": "In Progress", "Wann zuletzt geändert": "2026-01-22"},
        {"ProjektNr": "SW-002", "ÄnderungsID": "A-010", "Kurzbeschreibung": "Kundenwunsch Review", "Status": "Open", "Wann zuletzt geändert": "2026-01-18"},
        {"ProjektNr": "SW-003", "ÄnderungsID": "A-020", "Kurzbeschreibung": "Freigabe vorbereiten", "Status": "Planned", "Wann zuletzt geändert": "2026-01-10"},
    ])

    topics = pd.DataFrame([
        {"ProjektNr": "SW-001", "ThemenblattID": "TB-001", "Titel": "Projektplanung", "Status": "Open", "Owner": "Du", "LetzteÄnderung": "2026-01-21", "Beschreibung": "Planung, Termine, Meilensteine."},
        {"ProjektNr": "SW-001", "ThemenblattID": "TB-002", "Titel": "Kostenanalyse", "Status": "In Bearbeitung", "Owner": "Du", "LetzteÄnderung": "2026-01-23", "Beschreibung": "Analyse der Projektkosten und Budgetabweichungen."},
        {"ProjektNr": "SW-001", "ThemenblattID": "TB-005", "Titel": "Risikomanagement", "Status": "Open", "Owner": "Max", "LetzteÄnderung": "2026-01-19", "Beschreibung": "Risiken, Maßnahmen, Verantwortliche."},
        {"ProjektNr": "SW-002", "ThemenblattID": "TB-007", "Titel": "Qualitätskontrolle", "Status": "Done", "Owner": "Du", "LetzteÄnderung": "2026-01-15", "Beschreibung": "Qualitätsprüfungen und Nachweise."},
    ])

    lop = pd.DataFrame([
        {"ProjektNr": "SW-001", "Aufgabe": "Termin mit Einkauf", "Status": "Open", "Verantwortlich": "Du"},
        {"ProjektNr": "SW-001", "Aufgabe": "Kostenpositionen abstimmen", "Status": "In Progress", "Verantwortlich": "Max"},
        {"ProjektNr": "SW-002", "Aufgabe": "Dokumente sammeln", "Status": "Planned", "Verantwortlich": "Du"},
    ])

    return projects, change_list, topics, lop


if "data_initialized" not in st.session_state:
    st.session_state.projects, st.session_state.change_list, st.session_state.topics, st.session_state.lop = seed_data()
    st.session_state.data_initialized = True

# Selected context
if "selected_project" not in st.session_state:
    st.session_state.selected_project = st.session_state.projects.iloc[0]["ProjektNr"]

if "selected_topic_id" not in st.session_state:
    st.session_state.selected_topic_id = None

# -----------------------------
# Helper UI components
# -----------------------------
def header_bar(title: str):
    col1, col2 = st.columns([0.75, 0.25])
    with col1:
        st.markdown(f"## {title}")
    with col2:
        st.markdown("<div style='text-align:right; font-weight:600;'>Sonderwunsch</div>", unsafe_allow_html=True)
    st.divider()

def project_nav_buttons():
    st.markdown("#### Zum Projekt")
    st.caption(f"Aktives Projekt: **{st.session_state.selected_project}**")

    b1 = st.button("Projektplan", use_container_width=True)
    b2 = st.button("Änderungsliste", use_container_width=True)
    b3 = st.button("Kalkulationsvorlage", use_container_width=True)
    b4 = st.button("Teams", use_container_width=True)
    b5 = st.button("Projektorganigramm", use_container_width=True)
    b6 = st.button("LOP", use_container_width=True)

    if b1: st.session_state.page = "Projektplan"
    if b2: st.session_state.page = "Änderungsliste"
    if b3: st.session_state.page = "Kalkulationsvorlage"
    if b4: st.session_state.page = "Teams"
    if b5: st.session_state.page = "Projektorganigramm"
    if b6: st.session_state.page = "LOP"

def ensure_page():
    if "page" not in st.session_state:
        st.session_state.page = "Projektübersicht"

# -----------------------------
# Page: Ebene 1 - Projektübersicht
# -----------------------------
def page_project_overview():
    header_bar("Projektübersicht – One-Off Projekte (Demo)")

    left, right = st.columns([0.75, 0.25], gap="large")

    with left:
        df = st.session_state.projects.copy()

        # Simple search/filter row
        c1, c2 = st.columns([0.6, 0.4])
        with c1:
            q = st.text_input("Projekt suchen (ProjektNr / Kunde / Status)", "")
        with c2:
            status_filter = st.selectbox("Status Filter", ["Alle"] + sorted(df["Status"].unique().tolist()))

        if q.strip():
            ql = q.strip().lower()
            df = df[df.apply(lambda r: ql in " ".join(map(str, r.values)).lower(), axis=1)]

        if status_filter != "Alle":
            df = df[df["Status"] == status_filter]

        st.dataframe(df, use_container_width=True, hide_index=True)

        # Selection (simple)
        st.markdown("**Projekt auswählen:**")
        project_options = st.session_state.projects["ProjektNr"].tolist()
        st.session_state.selected_project = st.selectbox(
            "Aktives Projekt",
            options=project_options,
            index=project_options.index(st.session_state.selected_project),
            label_visibility="collapsed"
        )

    with right:
        st.markdown("### Aktionen")
        with st.expander("+ Neues Projekt anlegen", expanded=False):
            with st.form("new_project"):
                pnr = st.text_input("ProjektNr (z. B. SW-012)")
                cpm = st.text_input("CPM (optional)")
                kunde = st.text_input("Kunde")
                wu = st.text_input("Werksunikat")
                status = st.selectbox("Status", ["Open", "In Progress", "Planned", "Done"])
                submitted = st.form_submit_button("Projekt speichern")
                if submitted:
                    if not pnr:
                        st.error("Bitte ProjektNr eingeben.")
                    else:
                        new_row = {"ProjektNr": pnr, "CPM": cpm, "Kunde": kunde, "Werksunikat": wu, "Status": status}
                        st.session_state.projects = pd.concat([st.session_state.projects, pd.DataFrame([new_row])], ignore_index=True)
                        st.success("Projekt angelegt (Demo).")

        st.divider()
        project_nav_buttons()

# -----------------------------
# Page: Ebene 2 - Projektplan (Dummy)
# -----------------------------
def page_project_plan():
    header_bar("Projektplan")
    st.info("Demo: Hier könnte entweder eine kleine eingebettete Tabelle stehen oder ein Link zur Excel-Datei.")
    st.caption("Tipp für Demo: zeige 5 Meilensteine in einer Tabelle, später Datenübernahme möglich.")

# -----------------------------
# Page: Ebene 2 - Kalkulationsvorlage (Dummy)
# -----------------------------
def page_costing():
    header_bar("Kalkulationsvorlage")
    st.info("Demo: Link zur Kalkulations-Excel oder kleine Beispiel-Tabelle (Position, Menge, Preis).")

# -----------------------------
# Page: Ebene 2 - Teams (Dummy)
# -----------------------------
def page_teams():
    header_bar("Teams (Ordnerstruktur)")
    st.info("Demo: Link zur Teams/SharePoint-Ordnerstruktur. Optional: zeige die wichtigsten Ordner als Liste.")

# -----------------------------
# Page: Ebene 2 - Projektorganigramm (Dummy)
# -----------------------------
def page_org():
    header_bar("Projektorganigramm")
    st.info("Demo: Screenshot/Diagramm oder Tabelle (Rolle, Name, Bereich).")

# -----------------------------
# Page: Ebene 2 - LOP (Open Tasks)
# -----------------------------
def page_lop():
    header_bar("LOP – Offene Aufgaben")
    df = st.session_state.lop
    df = df[df["ProjektNr"] == st.session_state.selected_project].copy()
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.caption("Demo: Aufgaben können sich über Projekt/Änderungen erstrecken. Für jetzt: Projektfilter.")

# -----------------------------
# Page: Ebene 2 - Änderungsliste (mit Buttons zu Ebene 3)
# -----------------------------
def page_change_list():
    header_bar("Änderungsliste")

    left, mid, right = st.columns([0.2, 0.6, 0.2], gap="large")

    with left:
        st.markdown("### Aktionen")
        st.button("+ neues Objekt", use_container_width=True)

        st.markdown("### Objekt suchen")
        q = st.text_input("Suche", placeholder="z. B. A-001 oder Text…")
        st.button("Suchen", use_container_width=True)

    with mid:
        df = st.session_state.change_list
        df = df[df["ProjektNr"] == st.session_state.selected_project].copy()

        if q.strip():
            ql = q.strip().lower()
            df = df[df.apply(lambda r: ql in " ".join(map(str, r.values)).lower(), axis=1)]

        st.dataframe(df.drop(columns=["ProjektNr"]), use_container_width=True, hide_index=True)

    with right:
        st.markdown("### Weiterführend")
        if st.button("CPM", use_container_width=True):
            st.session_state.page = "CPM"
        if st.button("Laufwerk", use_container_width=True):
            st.session_state.page = "Laufwerk"
        if st.button("Themenblätter", use_container_width=True):
            st.session_state.page = "Themenblätter"

# -----------------------------
# Page: Ebene 3 - CPM (Dummy)
# -----------------------------
def page_cpm():
    header_bar("CPM")
    st.info("Demo: Link zu SAP PT1 (CPM) oder Screenshot. Später: echte Integration.")
    st.caption("Für Demo reicht ein 'Open CPM' Button, der einen Link öffnet.")

# -----------------------------
# Page: Ebene 3 - Laufwerk (Dummy)
# -----------------------------
def page_drive():
    header_bar("Laufwerk")
    st.info("Demo: Link zur Backbone / Datenablage / Projektordnerstruktur.")

# -----------------------------
# Page: Ebene 3 - Themenblätter (Sidebar links wie Skizze)
# -----------------------------
def page_topics():
    header_bar("Themenblatt Details")

    # Left collapsible sidebar inside main area
    left, right = st.columns([0.25, 0.75], gap="large")

    with left:
        st.markdown("###")
        if st.button("+ Neues Themenblatt", use_container_width=True):
            st.session_state.selected_topic_id = "__NEW__"

        st.markdown("#### Themenblätter suchen")
        search_key = st.text_input("Suchbegriff", placeholder="TB-002 ...")
        if st.button("Suchen", use_container_width=True):
            # just keeps search_key in state (Streamlit reruns anyway)
            st.session_state.topic_search = search_key

        st.divider()
        st.markdown("#### Deine Themenblätter:")
        df = st.session_state.topics
        df = df[(df["ProjektNr"] == st.session_state.selected_project) & (df["Owner"] == "Du")].copy()

        # Filter by search if provided
        key = st.session_state.get("topic_search", "").strip()
        if key:
            kl = key.lower()
            df = df[df["ThemenblattID"].str.lower().str.contains(kl) | df["Titel"].str.lower().str.contains(kl)]

        # List items
        if df.empty:
            st.caption("Keine Themenblätter gefunden.")
        else:
            for _, row in df.iterrows():
                label = f'{row["ThemenblattID"]} – {row["Titel"]}'
                if st.button(label, use_container_width=True):
                    st.session_state.selected_topic_id = row["ThemenblattID"]

    with right:
        # Right content panel
        df_all = st.session_state.topics
        df_p = df_all[df_all["ProjektNr"] == st.session_state.selected_project].copy()

        if st.session_state.selected_topic_id == "__NEW__":
            st.subheader("Neues Themenblatt")
            with st.form("new_topic"):
                tbid = st.text_input("Themenblatt-ID (Primärschlüssel)", placeholder="TB-010")
                title = st.text_input("Titel")
                status = st.selectbox("Status", ["Open", "In Bearbeitung", "Done"])
                owner = st.text_input("Owner", value="Du")
                desc = st.text_area("Beschreibung")
                saved = st.form_submit_button("Speichern")
                if saved:
                    if not tbid:
                        st.error("Bitte Themenblatt-ID angeben.")
                    else:
                        new_row = {
                            "ProjektNr": st.session_state.selected_project,
                            "ThemenblattID": tbid,
                            "Titel": title,
                            "Status": status,
                            "Owner": owner,
                            "LetzteÄnderung": str(date.today()),
                            "Beschreibung": desc
                        }
                        st.session_state.topics = pd.concat([st.session_state.topics, pd.DataFrame([new_row])], ignore_index=True)
                        st.success("Themenblatt angelegt (Demo).")
                        st.session_state.selected_topic_id = tbid

        elif st.session_state.selected_topic_id:
            topic = df_p[df_p["ThemenblattID"] == st.session_state.selected_topic_id]
            if topic.empty:
                st.info("Bitte links ein Themenblatt auswählen.")
            else:
                row = topic.iloc[0]
                st.subheader(f'{row["ThemenblattID"]}: {row["Titel"]}')
                c1, c2 = st.columns([0.7, 0.3])
                with c1:
                    st.markdown(f"**Status:** {row['Status']}")
                    st.markdown(f"**Owner:** {row['Owner']}")
                    st.markdown(f"**Letzte Änderung:** {row['LetzteÄnderung']}")
                with c2:
                    st.button("Bearbeiten", use_container_width=True)
                    st.button("Schließen", use_container_width=True)

                st.divider()
                st.markdown("**Beschreibung**")
                st.write(row["Beschreibung"])
        else:
            st.info("Links ein Themenblatt auswählen oder oben ein neues anlegen.")

# -----------------------------
# Sidebar (global navigation)
# -----------------------------
def sidebar_global():
    with st.sidebar:
        st.title("Navigation")
        st.caption("Demo-Prototyp")

        # Jump between main pages
        st.session_state.page = st.radio(
            "Seite",
            options=[
                "Projektübersicht",
                "Projektplan",
                "Änderungsliste",
                "Kalkulationsvorlage",
                "Teams",
                "Projektorganigramm",
                "LOP",
                "CPM",
                "Laufwerk",
                "Themenblätter",
            ],
            index=[
                "Projektübersicht",
                "Projektplan",
                "Änderungsliste",
                "Kalkulationsvorlage",
                "Teams",
                "Projektorganigramm",
                "LOP",
                "CPM",
                "Laufwerk",
                "Themenblätter",
            ].index(st.session_state.get("page", "Projektübersicht"))
        )

        st.divider()
        # Project context
        st.markdown("### Aktives Projekt")
        project_options = st.session_state.projects["ProjektNr"].tolist()
        st.session_state.selected_project = st.selectbox(
            "Projekt",
            options=project_options,
            index=project_options.index(st.session_state.selected_project),
            label_visibility="collapsed",
        )
        st.caption("Wechsel wirkt auf Änderungs- und Themenblatt-Daten.")

# -----------------------------
# Router
# -----------------------------
ensure_page()
sidebar_global()

page = st.session_state.page

if page == "Projektübersicht":
    page_project_overview()
elif page == "Projektplan":
    page_project_plan()
elif page == "Änderungsliste":
    page_change_list()
elif page == "Kalkulationsvorlage":
    page_costing()
elif page == "Teams":
    page_teams()
elif page == "Projektorganigramm":
    page_org()
elif page == "LOP":
    page_lop()
elif page == "CPM":
    page_cpm()
elif page == "Laufwerk":
    page_drive()
elif page == "Themenblätter":
    page_topics()
else:
    page_project_overview()



# To run the app, use the command:
# python3 -m streamlit run Lion/app.py