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
    rows = [{
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
    }]

    special = {2: "993351201OC001", 8: "993351202OC001"}
    eink_cycle = ["P2", "PW", "PK"]

    for i in range(2, 22):
        rows.append({
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
        })

    return pd.DataFrame(rows)[TABLE_COLS]


def _explorer_df(kind):
    base = date.today()
    items = []
    names = ["Datei1.xlsx", "Datei2.pdf", "Dokument.txt", "Liste.csv", "Bild.png"]

    for i, n in enumerate(names):
        items.append({
            "Name": f"{kind}_{n}",
            "Änderungsdatum": (base - timedelta(days=i)).strftime("%d.%m.%Y"),
            "Typ": "Datei",
            "Größe": f"{random.randint(20,500)} KB"
        })

    return pd.DataFrame(items)


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
def _header():
    st.markdown("## Classic Parts Monitor")
    st.markdown(
        f"<div style='margin-top:-6px;font-size:0.9rem;opacity:0.7;'>"
        f"Stand: {date.today().strftime('%d.%m.%Y')}"
        f"</div>",
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height:15px'></div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([7, 1.5, 1.5])

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
# NEW CPM DIALOG (FIXED VERSION)
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
            st.session_state.cpm_df = pd.concat(
                [df, pd.DataFrame([new_row])],
                ignore_index=True,
            )
            st.rerun()


# ---------------------------------------------------------
# MAIN TABLE
# ---------------------------------------------------------
def _main():
    if "cpm_df" not in st.session_state:
        st.session_state.cpm_df = _make_rows()

    df = st.session_state.cpm_df

    st.dataframe(
        df,
        height=650,
        use_container_width=True,
        hide_index=True,
    )

    if st.button("➕ Neues CPM anlegen"):
        _render_new_modal()


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
    st.session_state.setdefault("cpm_view", "MAIN")

    _header()

    if st.session_state.cpm_view == "MAIN":
        _main()
    else:
        _explorer(st.session_state.cpm_view)
