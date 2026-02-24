import streamlit as st
import pandas as pd
from datetime import date, timedelta
import random

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------
TABLE_COLS = [
    "Stat. Up",
    "CPM",
    "Unterpunkt",
    "Materialkurztext",
    "Teilenummer alt",
    "Teilenummer neu",
    "Liefer. / Standort",
    "Eink.",
    "Ter. Anlief",
    "Text",
]

EXPLORER_COLS = ["Name", "Änderungsdatum", "Typ", "Größe"]


# ---------------------------------------------------------
# DUMMY DATA
# ---------------------------------------------------------
def _random_part_alt():
    return f"{random.randint(10_000_000, 99_999_999)}XX"


def _random_date():
    base = date(2021, 5, 28)
    d = base + timedelta(days=random.randint(0, 2))
    return d.strftime("%d.%m.%Y")


def _make_rows():
    rows = [
        {
            "Stat. Up": 131,
            "CPM": 15078,
            "Unterpunkt": 1,
            "Materialkurztext": "",
            "Teilenummer alt": "99361130XX",
            "Teilenummer neu": "993351201OC001",
            "Liefer. / Standort": "SILVER FALCON GMBH",
            "Eink.": "PW",
            "Ter. Anlief": "30.05.2021",
            "Text": "IWAS AUFTRAG GEBUCHT",
        }
    ]

    special = {2: "993351201OC001", 8: "993351202OC001"}
    eink_cycle = ["P2", "PW", "PK"]

    for i in range(2, 22):
        rows.append(
            {
                "Stat. Up": random.choice([139, 131, 122]),
                "CPM": 15078,
                "Unterpunkt": i,
                "Materialkurztext": "",
                "Teilenummer alt": _random_part_alt(),
                "Teilenummer neu": special.get(i, ""),
                "Liefer. / Standort": "SILVER FALCON GMBH",
                "Eink.": eink_cycle[(i - 2) % 3],
                "Ter. Anlief": _random_date(),
                "Text": "IWAS AUFTRAG GEBUCHT",
            }
        )

    return pd.DataFrame(rows)[TABLE_COLS]


def _explorer_df(kind):
    base = date.today()
    items = []
    names = ["Datei1.xlsx", "Datei2.pdf", "Dokument.txt", "Liste.csv", "Bild.png"]

    for i, n in enumerate(names):
        items.append(
            {
                "Name": f"{kind}_{n}",
                "Änderungsdatum": (base - timedelta(days=i)).strftime("%d.%m.%Y"),
                "Typ": "Datei",
                "Größe": f"{random.randint(20, 500)} KB",
            }
        )

    return pd.DataFrame(items)[EXPLORER_COLS]


def _make_detail_log_df():
    rows = []
    base = date.today()
    texts = [
        "VORBEREITUNG FÜR CRK-ENTSCHEID ABGESCHLOSSEN",
        "CRK-ENTSCHEID LÄUFT VOR",
        "ÄNDERUNGSMANAGEMENT ABGESCHLOSSEN",
        "IWAS AUFTRAG GEBUCHT",
        "RÜCKFRAGE LIEFERANT / FREIGABE AUSSTEHEND",
        "PRÜFUNG TECHNIK / ZEICHNUNG",
    ]
    for i in range(1, 13):
        rows.append(
            {
                "ASN Datum AS": (base - timedelta(days=(18 - i))).strftime("%d.%m.%Y"),
                "A. v. Ber": random.choice(["P40", "P20", "SOLO.", "E", "I"]),
                "Text": random.choice(texts),
                "Stat": "🟢",
                "Zieltermin": (base + timedelta(days=random.randint(1, 30))).strftime("%d.%m.%Y"),
            }
        )
    return pd.DataFrame(rows)


# ---------------------------------------------------------
# STYLE (SAP/Explorer-ish look)
# ---------------------------------------------------------
def _inject_style():
    st.markdown(
        """
        <style>
          .sap-title {
            font-weight: 700;
            font-size: 1.05rem;
            padding: 6px 10px;
            background: linear-gradient(to bottom, #cfe1f3, #b7d0ea);
            border: 1px solid #9eb7d3;
            border-radius: 4px;
            margin-bottom: 10px;
          }
          .sap-box {
            border: 1px solid #c7d3e3;
            background: #eef4fb;
            border-radius: 4px;
            padding: 10px;
          }
          .sap-box + .sap-box {
            margin-top: 10px;
          }
          .sap-label {
            font-size: 0.78rem;
            opacity: 0.85;
            margin-bottom: 2px;
          }
          .sap-btn-col button {
            width: 100%;
            margin-bottom: 6px;
          }
          .tiny-note {
            margin-top:-6px;
            font-size:0.9rem;
            opacity:0.7;
          }
          .table-wrap {
            border: 1px solid #c7d3e3;
            background: #f6f9fd;
            border-radius: 4px;
            padding: 8px;
          }
          .crumb {
            font-size: 0.9rem;
            opacity: 0.75;
            margin-bottom: 8px;
          }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
def _header():
    st.markdown("## Classic Parts Monitor")
    st.markdown(
        f"<div class='tiny-note'>Stand: {date.today().strftime('%d.%m.%Y')}</div>",
        unsafe_allow_html=True,
    )

    # Buttons etwas tiefer setzen
    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([7, 1.6, 1.6])
    with c2:
        if st.button("PDMU", use_container_width=True):
            st.session_state.cpm_view = "PDMU"
            st.rerun()
    with c3:
        if st.button("Anhang", use_container_width=True):
            st.session_state.cpm_view = "ANHANG"
            st.rerun()

    st.divider()


# ---------------------------------------------------------
# NEW CPM DIALOG
# ---------------------------------------------------------
@st.dialog("Neues CPM anlegen")
def _render_new_modal():
    new_row = {}
    for col in TABLE_COLS:
        new_row[col] = st.text_input(col)

    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("Abbrechen", use_container_width=True):
            st.rerun()
    with c2:
        if st.button("Speichern", use_container_width=True):
            df = st.session_state.cpm_df
            st.session_state.cpm_df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            st.rerun()


# ---------------------------------------------------------
# DETAIL PAGE (full width, not a popup)
# ---------------------------------------------------------
def _render_detail_page(row: dict):
    st.markdown("<div class='sap-title'>CPM Punkt bearbeiten</div>", unsafe_allow_html=True)

    # Breadcrumb + back
    top_left, top_right = st.columns([0.75, 0.25])
    with top_left:
        st.markdown(
            f"<div class='crumb'>Classic Parts Monitor  ›  CPM {row.get('CPM','')} / Unterpunkt {row.get('Unterpunkt','')}</div>",
            unsafe_allow_html=True,
        )
    with top_right:
        if st.button("← Zurück zur Liste", use_container_width=True):
            st.session_state.cpm_view = "MAIN"
            st.session_state.cpm_selected_row = None
            st.rerun()

    # Layout: links Inhalte, rechts Button-Leiste
    left, right = st.columns([0.82, 0.18], gap="small")

    with left:
        # -------------------------
        # BOX OBEN
        # -------------------------
        st.markdown("<div class='sap-box'>", unsafe_allow_html=True)
        r1c1, r1c2, r1c3 = st.columns([0.33, 0.33, 0.34], gap="small")

        with r1c1:
            st.markdown("<div class='sap-label'>CPM Punkt</div>", unsafe_allow_html=True)
            st.text_input("", value=str(row.get("CPM", "")), disabled=True, key="d_cpm_punkt")

            st.markdown("<div class='sap-label'>Status</div>", unsafe_allow_html=True)
            st.text_input("", value=str(row.get("Stat. Up", "")), disabled=True, key="d_status")

            st.markdown("<div class='sap-label'>Anlass SOBE</div>", unsafe_allow_html=True)
            st.text_input("", value="SONDERWUNSCH", key="d_anlass_sobe")

            st.markdown("<div class='sap-label'>Techniker</div>", unsafe_allow_html=True)
            st.text_input("", value="TS JH: Peltke", key="d_techniker")

        with r1c2:
            st.markdown("<div class='sap-label'>Kunde / Modell</div>", unsafe_allow_html=True)
            st.text_input("", value="IDCA TRAZZI – UMSETZUNGSBAHR / BOM OC1", key="d_kunde_modell")

            st.markdown("<div class='sap-label'>IWAS-Nr.</div>", unsafe_allow_html=True)
            st.text_input("", value=str(random.randint(20000000, 29999999)), key="d_iwas_nr")

            st.markdown("<div class='sap-label'>SAP-Appl. Nr.</div>", unsafe_allow_html=True)
            st.text_input("", value=str(random.randint(22000000, 22999999)), key="d_sap_appl")

            st.markdown("<div class='sap-label'>Fzg. Aus. Dat.</div>", unsafe_allow_html=True)
            st.text_input("", value=(date.today() + timedelta(days=30)).strftime("%d.%m.%Y"), key="d_fzg_aus")

        with r1c3:
            st.markdown("<div class='sap-label'>Nr.</div>", unsafe_allow_html=True)
            st.text_input("", value=f"{row.get('CPM','')}/{row.get('Unterpunkt','')}", disabled=True, key="d_nr")
            st.markdown("<div class='sap-label'> </div>", unsafe_allow_html=True)
            st.text_input("", value="", key="d_blank1")
            st.text_input("", value="", key="d_blank2")
            st.text_input("", value="", key="d_blank3")

        st.markdown("</div>", unsafe_allow_html=True)

        # -------------------------
        # BOX MITTE
        # -------------------------
        st.markdown("<div class='sap-box'>", unsafe_allow_html=True)

        m1, m2, m3, m4 = st.columns([0.20, 0.22, 0.28, 0.30], gap="small")

        with m1:
            st.markdown("<div class='sap-label'>Vorgang</div>", unsafe_allow_html=True)
            st.text_input("", value="BESTELLUNGEN", key="m_vorgang")

            st.markdown("<div class='sap-label'>Unterpunkt</div>", unsafe_allow_html=True)
            st.text_input("", value=str(row.get("Unterpunkt", "")), disabled=True, key="m_unterpunkt")

            st.markdown("<div class='sap-label'>Status</div>", unsafe_allow_html=True)
            st.text_input("", value=str(row.get("Stat. Up", "")), disabled=True, key="m_status")

            st.markdown("<div class='sap-label'>Sparte</div>", unsafe_allow_html=True)
            st.text_input("", value="1", key="m_sparte")

        with m2:
            st.markdown("<div class='sap-label'>Lieferant</div>", unsafe_allow_html=True)
            st.text_input("", value=str(row.get("Liefer. / Standort", "")), key="m_lieferant")

            st.markdown("<div class='sap-label'>Teilenummer</div>", unsafe_allow_html=True)
            st.text_input("", value=str(row.get("Teilenummer alt", "")), key="m_teilenummer")

            st.markdown("<div class='sap-label'>Lief. Teil. Ben.</div>", unsafe_allow_html=True)
            st.text_input("", value="HECKLEUCHTE", key="m_lief_ben")

            st.markdown("<div class='sap-label'>Werksp. Mst.</div>", unsafe_allow_html=True)
            st.text_input("", value="", key="m_werksp")

        with m3:
            st.markdown("<div class='sap-label'>Bestell-Nr.</div>", unsafe_allow_html=True)
            st.text_input("", value="", key="m_bestellnr")

            st.markdown("<div class='sap-label'>Bestand</div>", unsafe_allow_html=True)
            st.text_input("", value="", key="m_bestand")

            st.markdown("<div class='sap-label'>Disponent</div>", unsafe_allow_html=True)
            st.text_input("", value="", key="m_disponent")

            st.markdown("<div class='sap-label'>Rst Pos.</div>", unsafe_allow_html=True)
            st.text_input("", value="0", key="m_rst_pos")

        with m4:
            st.markdown("<div class='sap-label'>Rst Menge</div>", unsafe_allow_html=True)
            st.text_input("", value="0,000", key="m_rst_menge")

            st.markdown("<div class='sap-label'>Prio</div>", unsafe_allow_html=True)
            st.text_input("", value=str(row.get("Eink.", "")), key="m_prio")

            st.markdown("<div class='sap-label'>Anforderer</div>", unsafe_allow_html=True)
            st.text_input("", value="M. BAUER", key="m_anforderer")

            st.markdown("<div class='sap-label'>LT Kundendat</div>", unsafe_allow_html=True)
            st.text_input("", value=(date.today() + timedelta(days=10)).strftime("%d.%m.%Y"), key="m_lt_kund")

        st.markdown("</div>", unsafe_allow_html=True)

        # -------------------------
        # TABELLE UNTEN
        # -------------------------
        st.markdown("<div class='table-wrap'>", unsafe_allow_html=True)
        log_df = _make_detail_log_df()
        st.dataframe(
            log_df,
            hide_index=True,
            use_container_width=True,
            height=360,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown("<div class='sap-box sap-btn-col'>", unsafe_allow_html=True)

        if st.button("AA / BA neu anlegen", use_container_width=True):
            st.toast("Dummy: AA/BA neu anlegen", icon="🧩")
        if st.button("AA / BA Bearbeiten", use_container_width=True):
            st.toast("Dummy: AA/BA bearbeiten", icon="🧩")
        if st.button("CPM Anhänge", use_container_width=True):
            st.toast("Dummy: Anhänge", icon="📎")
        if st.button("Status planen", use_container_width=True):
            st.toast("Dummy: Status planen", icon="🗓️")

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        if st.button("Neuer UP", use_container_width=True):
            st.toast("Dummy: Neuer UP", icon="➕")
        if st.button("UP -", use_container_width=True):
            st.toast("Dummy: UP -", icon="➖")
        if st.button("UP-Nr", use_container_width=True):
            st.toast("Dummy: UP-Nr", icon="🔢")

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        if st.button("Anwendungsdaten", use_container_width=True):
            st.toast("Dummy: Anwendungsdaten", icon="📄")
        if st.button("Statushistorie", use_container_width=True):
            st.toast("Dummy: Statushistorie", icon="🕘")

        st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------------
# MAIN TABLE
# ---------------------------------------------------------
def _main_table():
    if "cpm_df" not in st.session_state:
        st.session_state.cpm_df = _make_rows()

    df = st.session_state.cpm_df

    event = st.dataframe(
        df,
        height=650,
        use_container_width=True,
        hide_index=True,
        selection_mode="single-row",
        on_select="rerun",
        key="cpm_table_select",
    )

    # Button unten links (unter der Tabelle)
    left, _ = st.columns([0.22, 0.78])
    with left:
        if st.button("➕ Neues CPM anlegen", use_container_width=True):
            _render_new_modal()

    selected_rows = []
    try:
        selected_rows = event.selection.rows
    except Exception:
        selected_rows = []

    if selected_rows:
        idx = selected_rows[0]
        st.session_state.cpm_selected_row = df.iloc[idx].to_dict()
        st.session_state.cpm_view = "DETAIL"
        st.rerun()


# ---------------------------------------------------------
# EXPLORER VIEW
# ---------------------------------------------------------
def _explorer(kind):
    st.markdown(f"### {kind}")

    if st.button("← Zurück"):
        st.session_state.cpm_view = "MAIN"
        st.rerun()

    st.dataframe(
        _explorer_df(kind),
        height=550,
        use_container_width=True,
        hide_index=True,
    )


# ---------------------------------------------------------
# PUBLIC RENDER
# ---------------------------------------------------------
def render():
    _inject_style()

    st.session_state.setdefault("cpm_view", "MAIN")
    st.session_state.setdefault("cpm_selected_row", None)

    _header()

    view = st.session_state.cpm_view

    if view == "MAIN":
        _main_table()
    elif view == "DETAIL":
        row = st.session_state.cpm_selected_row or {}
        _render_detail_page(row)
    elif view in ("PDMU", "ANHANG"):
        _explorer(view)
    else:
        st.session_state.cpm_view = "MAIN"
        st.rerun()
