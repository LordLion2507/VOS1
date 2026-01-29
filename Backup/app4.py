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

a.demo-link {
  color: #1a73e8;
  text-decoration: underline;
  cursor: pointer;
}

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

/* LOP: horizontal scroll + sticky first column */
.lop-wrap { overflow-x: auto; border: 1px solid #E6E6E6; border-radius: 10px; }
.lop-table { border-collapse: collapse; width: 1600px; }
.lop-table th, .lop-table td { border: 1px solid #E6E6E6; padding: 10px; font-size: 14px; white-space: nowrap; }
.lop-table th { background: #F5F5F5; font-weight: 600; position: sticky; top: 0; z-index: 3; }
.lop-table td.sticky, .lop-table th.sticky { position: sticky; left: 0; background: #FFFFFF; z-index: 4; }
.lop-table th.sticky { background: #F5F5F5; }

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
st.session_state.setdefault("change_table_rows", [])     

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

        st.session_state.page = st.radio(
            "Seite",
            options=pages,
            index=pages.index(st.session_state.page) if st.session_state.page in pages else 0,
        )

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
# PAGE: Ebene 1 - Projektübersicht
# ---------------------------------------------------------
def page_project_overview():
    header_bar("Projektübersicht – One-Off Projekte")

    left, right = st.columns([0.75, 0.25], gap="large")

    with left:
        df = st.session_state.projects.copy()

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

        st.markdown('<div class="demo-card">', unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("**Projekt auswählen:**")
        project_options = st.session_state.projects["ProjektNr"].tolist()
        st.session_state.selected_project = st.selectbox(
            "Aktives Projekt",
            options=project_options,
            index=project_options.index(st.session_state.selected_project),
            label_visibility="collapsed",
        )

    with right:
        st.markdown('<div class="demo-card">', unsafe_allow_html=True)
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

        st.button("Projekt bearbeiten", use_container_width=True)

        st.divider()
        project_nav_box()
        st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------------
# PAGE: Projektplan 
# ---------------------------------------------------------
def page_project_plan():
    header_bar("Projektplan")
    st.info("Hier soll der spezifische Projektplan zu finden sein, je nachdem welches Projekt ausgewählt ist.")

    if os.path.exists(PROJECTPLAN_IMG):
        st.image(PROJECTPLAN_IMG, use_container_width=True)
    else:
        st.warning(f"Lege ein Bild unter **{PROJECTPLAN_IMG}** ab (Ordner `assets/`), dann wird es hier angezeigt.")


# ---------------------------------------------------------
# PAGE: Änderungsliste
# ---------------------------------------------------------
def page_change_list():
    header_bar("Änderungsliste")

    left, mid, right = st.columns([0.22, 0.58, 0.20], gap="large")

    with left:
        st.markdown('<div class="demo-card">', unsafe_allow_html=True)
        st.markdown("## Aktionen")
        st.button("neues Objekt", use_container_width=True)

        st.markdown("## Objekt suchen\n")
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

        show_df = df[["Option", "Beschreibung", "Kategorie", "Status", "Wann zuletzt geändert"]].copy()

        def _style_option(col):
            return [
                "color:#1a73e8; text-decoration: underline; font-weight: 500;" if col.name == "Option" else ""
                for _ in col
            ]

        styler = show_df.style.apply(_style_option, axis=0)

        event = st.dataframe(
            styler,
            use_container_width=True,
            hide_index=True,
            selection_mode="single-row",
            on_select="rerun",
            key="change_table",
        )

        # selection auswerten
        selected_rows = []
        try:
            selected_rows = event.selection.rows
        except Exception:
            selected_rows = []

        if selected_rows:
            st.session_state.change_preview_open = True
            st.session_state.change_table_rows = selected_rows

    with right:
        st.markdown('<div class="demo-card">', unsafe_allow_html=True)
        st.markdown("## Weiterführend\n")
        st.button("CPM", use_container_width=True, on_click=set_page, args=("CPM",))
        st.button("Laufwerk", use_container_width=True, on_click=set_page, args=("Laufwerk",))
        st.button("Themenblätter", use_container_width=True, on_click=set_page, args=("Themenblätter",))
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("")

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
                st.session_state.change_table_rows = []
                # optional: suche behalten, selection wird durch rerun eh neu gesetzt

            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.caption("Klicke in der Tabelle → Vorschau erscheint hier.")


# ---------------------------------------------------------
# PAGE: Kalkulationsvorlage 
# ---------------------------------------------------------
def page_costing():
    header_bar("Kalkulationsvorlage")

    base_cols = [
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

    if "costing_df" not in st.session_state:
        st.session_state.costing_df = pd.DataFrame(
            [
                {
                    "PAG Kostenblöcke": "One-Off",
                    "Anzahl Fahrzeuge": 1,
                    "Invest (Werkzeuge)": "",
                    "MEK (Teile Kunden Fahrzeuge) Nicht COP-A": "",
                    "MEK COP-A inkl. Marge": "",
                    "PT-Mat": "",
                    "Eigen-E": "",
                    "Fremd-E": "",
                    "Gewerbliche Stunden": "",
                    "Qualität, Bemusterung": "",
                    "Prüfkosten, Versuchsträger": "",
                    "Equipment, Anlagen, Prüfstände": "",
                    "Zertifizierung, Zulassung": "",
                    "Fahrzeugdokumentation": "",
                    "Marketing und Kundenbegeisterung": "",
                    "FTE indirekt (PAG)": "",
                    "Eingabe (leer)": "",
                }
            ],
            columns=base_cols,
        )

    edited = st.data_editor(
        st.session_state.costing_df,
        use_container_width=True,
        num_rows="dynamic",
        hide_index=True,
    )
    st.session_state.costing_df = edited


# ---------------------------------------------------------
# PAGE: LOP 
# ---------------------------------------------------------
def render_lop_table(df: pd.DataFrame):
    cols = list(df.columns)
    sticky_col = cols[0] if cols else None

    thead = "<tr>" + "".join(
        [f"<th class='{'sticky' if c == sticky_col else ''}'>{html.escape(c)}</th>" for c in cols]
    ) + "</tr>"

    body_rows = ""
    for _, r in df.iterrows():
        tds = ""
        for c in cols:
            val = "" if pd.isna(r[c]) else str(r[c])
            cls = "sticky" if c == sticky_col else ""
            tds += f"<td class='{cls}'>{html.escape(val)}</td>"
        body_rows += f"<tr>{tds}</tr>"

    st.markdown(
        f"""
<div class="lop-wrap">
  <table class="lop-table">
    <thead>{thead}</thead>
    <tbody>{body_rows}</tbody>
  </table>
</div>
""",
        unsafe_allow_html=True,
    )

def page_lop():
    header_bar("LOP")
    df = st.session_state.lop.copy()
    while len(df) < 10:
        df = pd.concat([df, df.iloc[[len(df) % 3]].copy()], ignore_index=True)
    render_lop_table(df)

# ---------------------------------------------------------
# PAGE: Laufwerk
# ---------------------------------------------------------
def page_drive():
    header_bar("Laufwerk")
    st.info("Ordnerstruktur nachbauen: in Ordner reinklicken, leerer Ordner, zurück.")

    bc = " / ".join(st.session_state.drive_path) if st.session_state.drive_path else "Root"
    st.caption(f"Pfad: **{bc}**")

    c1, c2 = st.columns([0.15, 0.85])
    with c1:
        if st.button("Back", use_container_width=True, disabled=(len(st.session_state.drive_path) == 0)):
            st.session_state.drive_path.pop()

    node = st.session_state.drive_tree
    for p in st.session_state.drive_path:
        node = node.get(p, {})

    st.markdown('<div class="demo-card">', unsafe_allow_html=True)
    if not node:
        st.markdown("Leerer Ordner (Demo).")
        st.caption("Hier würden Dateien/Links erscheinen. Für die Demo reicht 'leer' + Navigation.")
    else:
        for folder in node.keys():
            colA, colB = st.columns([0.75, 0.25])
            with colA:
                st.markdown(
                    f"<div class='drive-item'><div class='drive-title'>✿ {html.escape(folder)}</div>"
                    f"<div class='drive-meta'>Dateiordner</div></div>",
                    unsafe_allow_html=True,
                )
            with colB:
                if st.button("Öffnen", key=f"open_{folder}", use_container_width=True):
                    st.session_state.drive_path.append(folder)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Dummy pages
# ---------------------------------------------------------
def page_teams():
    header_bar("Teams")
    st.info("Struktur aus Teams hier einzubetten.")

def page_org():
    header_bar("Projektorganigramm")
    st.info("Projektorganigramm hier zu finden.")

def page_cpm():
    header_bar("CPM")
    st.info("CPM hier einzufügen.")

# ---------------------------------------------------------
# PAGE: Themenblätter (links: Neues/Suche/Deine; rechts: Details)
# ---------------------------------------------------------
def page_topics():
    header_bar("Themenblatt Details")

    left, right = st.columns([0.25, 0.75], gap="large")

    with left:
        st.markdown('<div class="demo-card">', unsafe_allow_html=True)
        if st.button("+ Neues Themenblatt", use_container_width=True):
            st.session_state.selected_topic_id = "__NEW__"

        st.markdown("#### Themenblätter suchen")
        search_key = st.text_input("Suche", value=st.session_state.topic_search, placeholder="TB-014 oder Begriff…")
        if st.button("Suchen", use_container_width=True):
            st.session_state.topic_search = search_key

        st.divider()
        st.markdown("#### Deine Themenblätter:")
        df = st.session_state.topics
        df = df[(df["ProjektNr"] == st.session_state.selected_project) & (df["Owner"] == "Du")].copy()

        key = st.session_state.topic_search.strip()
        if key:
            kl = key.lower()
            df = df[df["ThemenblattID"].str.lower().str.contains(kl) | df["Titel"].str.lower().str.contains(kl)]

        if df.empty:
            st.caption("Keine Themenblätter gefunden.")
        else:
            for _, row in df.iterrows():
                label = f'{row["ThemenblattID"]} – {row["Titel"]}'
                if st.button(label, use_container_width=True, key=f"tb_{row['ThemenblattID']}"):
                    st.session_state.selected_topic_id = row["ThemenblattID"]

        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="demo-card">', unsafe_allow_html=True)

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
                            "Beschreibung": desc,
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
                    if st.button("Schließen", use_container_width=True):
                        st.session_state.selected_topic_id = None

                st.divider()
                st.markdown("**Beschreibung**")
                st.write(row["Beschreibung"])

        else:
            st.info("Links ein Themenblatt auswählen oder oben ein neues anlegen.")

        st.markdown("</div>", unsafe_allow_html=True)

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
# python3 -m streamlit run Lion/app4.py
