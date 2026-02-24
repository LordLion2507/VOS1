import streamlit as st
import pandas as pd
from datetime import date, timedelta
import random

# ---------------------------------------------------------
# Helpers: Dummy Data
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


def _random_part_alt() -> str:
    # 8 random digits + XX
    return f"{random.randint(10_000_000, 99_999_999)}XX"


def _random_date_str_between_2021_05_28_and_30() -> str:
    base = date(2021, 5, 28)
    d = base + timedelta(days=random.randint(0, 2))  # 28..30
    return d.strftime("%d.%m.%Y")


def _make_dummy_rows() -> pd.DataFrame:
    rows = []

    # Beispielzeile (von dir vorgegeben)
    rows.append(
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
    )

    # 20 weitere Dummy-Zeilen
    # Hinweis: "Teilenummer neu" -> 2x irgendwo platzieren, einmal mit 1 Ziffer geändert
    # Wir platzieren:
    # - Zeile 2: 993351201OC001
    # - Zeile 8: 993351202OC001 (1 Ziffer geändert)
    special_map = {2: "993351201OC001", 8: "993351202OC001"}

    eink_cycle = ["P2", "PW", "PK"]

    for i in range(2, 22):  # 2..21 = 20 Zeilen
        rows.append(
            {
                "Stat. Up": random.choice([139, 131, 122]),
                "CPM": 15078,
                "Unterpunkt": i,
                "Materialkurztext": "",
                "Teilenummer alt": _random_part_alt(),
                "Teilenummer neu": special_map.get(i, ""),
                "Liefer. / Standort": "SILVER FALCON GMBH",
                "Eink.": eink_cycle[(i - 2) % len(eink_cycle)],
                "Ter. Anlief": _random_date_str_between_2021_05_28_and_30(),
                "Text": "IWAS AUFTRAG GEBUCHT",
            }
        )

    return pd.DataFrame(rows)[TABLE_COLS]


def _make_explorer_df(kind: str) -> pd.DataFrame:
    # kind: "PDMU" oder "Anhang"
    # Explorer-Style Tabelle: Name | Änderungsdatum | Typ | Größe
    base_date = date.today()
    items = []

    if kind == "PDMU":
        names = [
            "PDMU_Stueckliste.xlsx",
            "PDMU_Aenderungsstand.pdf",
            "PDMU_Freigabe.txt",
            "PDMU_Bericht_001.docx",
            "PDMU_Export.csv",
        ]
    else:
        names = [
            "Anhang_Foto_01.png",
            "Anhang_Skizze.pdf",
            "Anhang_Notizen.txt",
            "Anhang_Berechnung.xlsx",
            "Anhang_Anforderung.docx",
        ]

    types = {
        ".xlsx": "Microsoft Excel Worksheet",
        ".pdf": "PDF-Datei",
        ".txt": "Textdokument",
        ".docx": "Microsoft Word Document",
        ".csv": "CSV-Datei",
        ".png": "PNG-Datei",
    }

    for idx, name in enumerate(names, start=1):
        ext = "." + name.split(".")[-1]
        items.append(
            {
                "Name": name,
                "Änderungsdatum": (base_date - timedelta(days=idx)).strftime("%d.%m.%Y"),
                "Typ": types.get(ext, "Datei"),
                "Größe": f"{random.randint(12, 980)} KB",
            }
        )

    return pd.DataFrame(items)[EXPLORER_COLS]


# ---------------------------------------------------------
# UI: Header / Explorer View / Main Table
# ---------------------------------------------------------
def _render_header():
    # Links: Titel + Stand; rechts: Buttons
    left, right = st.columns([0.72, 0.28], vertical_alignment="top")

    with left:
        st.markdown("## Classic Parts Monitor")
        st.markdown(
            f"<div style='margin-top:-8px; font-size:0.9rem; opacity:0.75;'>"
            f"Stand: {date.today().strftime('%d.%m.%Y')}"
            f"</div>",
            unsafe_allow_html=True,
        )

    with right:
        # Buttons oben rechts
        r1, r2 = st.columns(2)
        with r1:
            if st.button("PDMU", use_container_width=True):
                st.session_state.cpm_view = "PDMU"
                st.rerun()
        with r2:
            if st.button("Anhang", use_container_width=True):
                st.session_state.cpm_view = "Anhang"
                st.rerun()

    st.markdown("---")


def _render_explorer(kind: str):
    # Explorer-Ansicht: oben links Name + Tabelle wie Windows Explorer
    st.markdown(f"### {kind}")

    if st.button("← Zurück", use_container_width=False):
        st.session_state.cpm_view = "MAIN"
        st.rerun()

    df = _make_explorer_df(kind)

    # Höhe setzen, damit scrollbars auftreten und Header sichtbar bleibt
    st.dataframe(
        df,
        hide_index=True,
        use_container_width=True,
        height=520,
    )


def _render_main_table():
    # große Tabelle, scrollbar, Header bleibt sichtbar (Streamlit macht das bei height)
    if "cpm_table_df" not in st.session_state:
        st.session_state.cpm_table_df = _make_dummy_rows()

    df = st.session_state.cpm_table_df

    # Optional: "sticky" Header + Scroll -> via height
    st.dataframe(
        df,
        hide_index=True,
        use_container_width=True,
        height=650,
    )


# ---------------------------------------------------------
# Public Render (called from Sonderwunsch router)
# ---------------------------------------------------------
def render():
    st.session_state.setdefault("cpm_view", "MAIN")

    _render_header()

    if st.session_state.cpm_view in ("PDMU", "Anhang"):
        _render_explorer(st.session_state.cpm_view)
    else:
        _render_main_table()
