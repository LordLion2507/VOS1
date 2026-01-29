import os
import html
from datetime import date
import pandas as pd
import streamlit as st

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Sonderwunsch – One-Off Projekte (Demo)",
    page_icon="🧩",
    layout="wide",
)

ASSETS_DIR = "assets"
PROJECTPLAN_IMG = os.path.join(ASSETS_DIR, "projektplan.png")
AENDERUNG_TEMPLATE_IMG = os.path.join(ASSETS_DIR, "aenderung_template.png")

# ---------------------------------------------------------
# GLOBAL CSS
# ---------------------------------------------------------
st.markdown(
    """
<style>
.block-container { padding-top: 1.2rem; padding-bottom: 2rem; }

.demo-card {
  border: 1px solid #E6E6E6;
  border-radius: 10px;
  padding: 14px 14px;
  background: #FFFFFF;
}

.sidebar-card {
  border: 1px solid #EAEAEA;
  border-radius: 10px;
  padding: 12px;
  background: #FAFAFA;
}

/* Änderungsliste Preview rechts unten */
.preview-box {
  border: 1px solid #E6E6E6;
  border-radius: 10px;
  background: #FFFFFF;
  height: 520px;
  padding: 10px;
}
.preview-title { font-weight: 700; margin-bottom: 6px; }
.preview-sub { color: #666; font-size: 13px; margin-bottom: 10px; }

/* LOP: horizontal scroll + sticky first column */
.lop-wrap { overflow-x: auto; border: 1px solid #E6E6E6; border-radius: 10px; }
.lop-table { border-collapse: collapse; width: 1600px; }
.lop-table th, .lop-table td { border: 1px solid #E6E6E6; padding: 10px; font-size: 14px; white-space: nowrap; }
.lop-table th { background: #F5F5F5; font-weight: 600; position: sticky; top: 0; z-index: 3; }
.lop-table td.sticky, .lop-table th.sticky { position: sticky; left: 0; background: #FFFFFF; z-index: 4; }
.lop-table th.sticky { background: #F5F5F5; }

/* Laufwerk */
.drive-item {
  padding: 10px 12px;
  border: 1px solid #E6E6E6;
  border-radius: 10px;
  margin-bottom: 8px;
  background: #FFFFFF;
}
.drive-title { font-weight: 650; }
.drive-meta { color:#666; font-size: 12px; }
</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# DATA SEED (Demo)
# ---------------------------------------------------------
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

    # Änderungsliste (Demo) – Option soll wie Hyperlink aussehen
    change_list = pd.DataFrame(
        [
            {"ProjektNr": "SW-001", "Option": "OE3-001", "Beschreibung": "Allgemeines/ Gesamtfahrzeug", "Kategorie": "-", "Status": "Open", "Wann zuletzt geändert": "2026-01-20"},
            {"ProjektNr": "SW-001", "Option": "OE3-002", "Beschreibung": "Konstruktion", "Kategorie": "-", "Status": "In Progress", "Wann zuletzt geändert": "2026-01-22"},
            {"ProjektNr": "SW-001", "Option": "OE3-003", "Beschreibung": "Zulassung, Gesetze und Normen", "Kategorie": "-", "Status": "Open", "Wann zuletzt geändert": "2026-01-18"},
            {"ProjektNr": "SW-002", "Option": "OE3-010", "Beschreibung": "Elektrik und Elektronik", "Kategorie": "-", "Status": "Planned", "Wann zuletzt geändert": "2026-01-10"},
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
                "Beschreibung": "Demo-Text …",
            }
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
            }
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


# ---------------------------------------------------------
# SESSION STATE INIT
# ---------------------------------------------------------
if "data_initialized" not in st.session_state:
    st.session_state.projects, st.session_state.change_list, st.session_state.topics, st.session_state.lop, st.session_state.drive_tree = seed_data()
    st.session_state.data_initialized = True

st.session_state.setdefault("page", "Projektübersicht")
st.session_state.setdefault("selected_project", st.session_state.projects.iloc[0]["ProjektNr"])
st.session_state.setdefault("selected_topic_id", None)
st.session_state.setdefault("topic_search", "")
st.session_state.setdefault("change_preview_open", False)
st.session_state.setdefault("drive_path", [])
st.session_state.setdefault("change_search", "")

# ---------------------------------------------------------
# UI HELPERS
# ---------------------------------------------------------
def header_bar(title: str):
    c1, c2 = st.columns([0.78, 0.22])
    with c1:
        st.markdown(f"# {title}")
    with c2:
        st.markdown("<div style='text-align:right; font-weight:700; padding-top:18px;'>Sonderwunsch</div>", unsafe_allow_html=True)
    st.divider()

def set_page(name: str):
    st.session_state.page = name

def project_nav_box():
    st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
    st.markdown("### Zum Projekt")
    st.caption(f"Aktives Projekt: **{st.session_state.selected_project}**")
    st.button("Projektplan", use_container_width=True, on_click=set_page, args=("Projektplan",))
    st.button("Änderungsliste", use_container_width=True, on_click=set_page, args=("Änderungsliste",))
    st.button("Kalkulationsvorlage", use_container_width=True, on_click=set_page, args=("Kalkulationsvorlage",))
    st.button("Teams", use_container_width=True, on_click=set_page, args=("Teams",))
    st.button("Projektorganigramm", use_container_width=True, on_click=set_page, args=("Projektorganigramm",))
    st.button("LOP", use_container_width=True, on_click=set_page, args=("LOP",))
    st.markdown("</div>", unsafe_allow_html=True)

def sidebar_global():
    with st.sidebar:
        st.title("Navigation")
        st.caption("Demo-Prototyp (lokal)")

        pages = [
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
        ]

        st.session_state.page = st.radio("Seite", options=pages, index=pages.index(st.session_state.page))

        st.divider()
        st.markdown("### Aktives Projekt")
        project_options = st.session_state.projects["ProjektNr"].tolist()
        st.session_state.selected_project = st.selectbox(
            "Projekt",
            options=project_options,
            index=project_options.index(st.session_state.selected_project),
            label_visibility="collapsed",
        )

# ---------------------------------------------------------
# PAGE: Projektübersicht
# ---------------------------------------------------------
def page_project_overview():
    header_bar("Projektübersicht – One-Off Projekte (Demo)")

    left, right = st.columns([0.75, 0.25], gap="large")
    with left:
        st.markdown('<div class="demo-card">', unsafe_allow_html=True)
        st.dataframe(st.session_state.projects, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="demo-card">', unsafe_allow_html=True)
        st.markdown("### Aktionen")
        st.button("+ Neues Projekt anlegen", use_container_width=True)
        st.button("Projekt bearbeiten", use_container_width=True)
        st.divider()
        project_nav_box()
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# PAGE: Projektplan (nur Bild)
# ---------------------------------------------------------
def page_project_plan():
    header_bar("Projektplan")
    st.info("Hier soll der spezifische Projektplan zu finden sein, je nachdem welches Projekt ausgewählt ist.")
    if os.path.exists(PROJECTPLAN_IMG):
        st.image(PROJECTPLAN_IMG, use_container_width=True)
    else:
        st.warning(f"Lege ein Bild unter **{PROJECTPLAN_IMG}** ab (assets/), dann wird es hier angezeigt.")

# ---------------------------------------------------------
# ✅ PAGE: Änderungsliste – FIX (gemäß Screenshot)
# ---------------------------------------------------------
def page_change_list():
    header_bar("Änderungsliste")

    # Layout wie im Screenshot: links Aktionen/Suche, Mitte Tabelle, rechts Weiterführend + Preview unten
    left, mid, right = st.columns([0.22, 0.58, 0.20], gap="large")

    with left:
        st.markdown('<div class="demo-card">', unsafe_allow_html=True)
        st.markdown("## Aktionen")
        st.button("neues Objekt", use_container_width=True)

        st.markdown("## Objekt\nsuchen")
        q = st.text_input("Suche", value=st.session_state.change_search, placeholder="z. B. OE3-001 oder Text…")
        if st.button("Suchen", use_container_width=True):
            st.session_state.change_search = q
        st.markdown("</div>", unsafe_allow_html=True)

    with mid:
        df = st.session_state.change_list
        df = df[df["ProjektNr"] == st.session_state.selected_project].copy()

        q = st.session_state.change_search.strip()
        if q:
            ql = q.lower()
            df = df[df.apply(lambda r: ql in " ".join(map(str, r.values)).lower(), axis=1)]

        # Nur die Spalten wie in deiner Beschreibung (Option muss wie Hyperlink aussehen)
        show_df = df[["Option", "Beschreibung", "Kategorie", "Status", "Wann zuletzt geändert"]].copy()

        # "Hyperlink-Look" für Option-Spalte (blau+underline)
        def _style_option(s):
            return [
                "color:#1a73e8; text-decoration: underline; font-weight: 500;" if s.name == "Option" else ""
                for _ in s
            ]

        styler = show_df.style.apply(_style_option, axis=0)

        # ✅ Wichtig: wir nutzen selection (click) statt echte Links → Preview rechts unten
        event = st.dataframe(
            styler,
            use_container_width=True,
            hide_index=True,
            selection_mode="single-row",
            on_select="rerun",
            key="change_table",
        )

        # Wenn irgendwo in der Tabelle geklickt wurde -> Preview öffnen (egal welcher "Option"-Klick)
        try:
            selected = event.selection.rows
        except Exception:
            selected = []

        if selected:
            st.session_state.change_preview_open = True

        st.caption("In der Demo reicht: Klick in der Tabelle (Option wirkt wie Link) → rechts unten öffnet die neue Seite (leeres Blatt).")

    with right:
        st.markdown('<div class="demo-card">', unsafe_allow_html=True)
        st.markdown("## Weiterführen\nd")
        st.button("CPM", use_container_width=True, on_click=set_page, args=("CPM",))
        st.button("Laufwerk", use_container_width=True, on_click=set_page, args=("Laufwerk",))
        st.button("Themenblätter", use_container_width=True, on_click=set_page, args=("Themenblätter",))
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("")

        # ✅ Rechts unten: "neue Seite" / leeres Blatt (wie gefordert: egal welcher Option-Link)
        if st.session_state.change_preview_open:
            st.markdown('<div class="preview-box">', unsafe_allow_html=True)
            st.markdown('<div class="preview-title">Vorschau</div>', unsafe_allow_html=True)
            st.markdown('<div class="preview-sub">Leeres Blatt (Demo) – egal welche Option.</div>', unsafe_allow_html=True)

            if os.path.exists(AENDERUNG_TEMPLATE_IMG):
                st.image(AENDERUNG_TEMPLATE_IMG, use_container_width=True)
            else:
                st.markdown(
                    """
<div style="border:1px dashed #BDBDBD; border-radius:10px; height:380px;
            display:flex; align-items:center; justify-content:center; color:#777;">
  (unausgefülltes Blatt)
</div>
""",
                    unsafe_allow_html=True,
                )

            if st.button("Vorschau schließen", use_container_width=True):
                st.session_state.change_preview_open = False
                # Selection reset (damit nicht sofort wieder aufspringt)
                st.session_state["change_table"] = {"selection": {"rows": []}}

            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.caption("Klicke in der Tabelle → Vorschau erscheint hier.")

# ---------------------------------------------------------
# Minimal-Placeholder Seiten
# ---------------------------------------------------------
def page_costing():
    header_bar("Kalkulationsvorlage")
    st.info("Platzhalter (unverändert).")

def page_teams():
    header_bar("Teams")
    st.info("Platzhalter.")

def page_org():
    header_bar("Projektorganigramm")
    st.info("Platzhalter.")

def page_lop():
    header_bar("LOP")
    st.info("Platzhalter.")

def page_cpm():
    header_bar("CPM")
    st.info("Platzhalter.")

def page_drive():
    header_bar("Laufwerk")
    st.info("Platzhalter.")

def page_topics():
    header_bar("Themenblatt Details")
    st.info("Platzhalter.")

# ---------------------------------------------------------
# ROUTER
# ---------------------------------------------------------
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

# Run:
# python3 -m streamlit run Lion/app3.py
