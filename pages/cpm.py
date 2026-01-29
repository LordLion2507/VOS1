import streamlit as st
import pandas as pd
from datetime import date
from shared.helpers import header_bar

# ---------------------------------------------------------
# CPM: Felddefinitionen (jeweils "von" + "bis")
# ---------------------------------------------------------
RANGE_FIELDS = [
    "CPM-Punkt",
    "Unterpunkt",
    "Teilenummer",
    "Status UP",
    "Reichweite (Jahre)",
    "Prio",
    "Disponent",
    "Einkäufer",
    "Techniker",
    "Produktmanager",
    "CLIX",
    "Datum angelegt (Status 000)",
    "Anlass",
    "Anlass SOBE",
    "Änd. Antrag",
    "Lieferanten-Nr.",
    "Kunde/Modell",
    "IWAS-Nr.",
    "Vorgang",
    "Anforderer",
    "Art Arbeitsschritt",
    "Verantwortlicher Bereich",
    "Status Arbeitsschritt",
    "Text Arbeitsschritt",
    "Zieltermin",
]

# Welche Spalten in der Tabelle sichtbar sein sollten
TABLE_COLS = [
    "CPM-ID",
    "CPM-Punkt",
    "Unterpunkt",
    "Teilenummer",
    "Status UP",
    "Prio_von",
    "Verantwortlicher Bereich",
    "Status Arbeitsschritt",
    "Zieltermin",
]

AKTIONEN = ["CPM-Punkt neu erfassen", "SOBE neu erfassen"]
ANZEIGEUMFANG = ["Nur UP-Auflösung", "aggregierte Anzeige", "Detailanzeige"]


# ---------------------------------------------------------
# Session Init + Dummy Rows
# ---------------------------------------------------------
def _make_empty_row(cpm_id: str) -> dict:
    row = {"CPM-ID": cpm_id}

    # Aktionen
    row["Aktion_CPM"] = False
    row["Aktion_SOBE"] = False

    # Anzeigeumfang: single value
    row["Anzeigeumfang"] = "Nur UP-Auflösung"

    # Range-Felder als _von/_bis
    for f in RANGE_FIELDS:
        row[f"{f}_von"] = ""
        row[f"{f}_bis"] = ""

    row["Datum angelegt (Status 000)_von"] = str(date.today())
    row["Datum angelegt (Status 000)_bis"] = ""
    return row


def _init_cpm():
    if "cpm_rows" not in st.session_state:
        r1 = _make_empty_row("CPM-001")
        r1.update(
            {
                "Aktion_CPM": True,
                "Anzeigeumfang": "Nur UP-Auflösung",
                "CPM-Punkt": "OE3-001",
                "Unterpunkt": "U-01",
                "Teilenummer": "9A1-807-221",
                "Status UP": "000",
                "Prio": "A",
                "Verantwortlicher Bereich": "Konstruktion",
                "Status Arbeitsschritt": "SOP",
                "Zieltermin": "2026-02-10",
            }
        )

        r2 = _make_empty_row("CPM-002")
        r2.update(
            {
                "Aktion_SOBE": True,
                "Anzeigeumfang": "aggregierte Anzeige",
                "CPM-Punkt_von": "OE3-007",
                "Unterpunkt_von": "U-03",
                "Teilenummer_von": "9A1-907-115",
                "Status UP_von": "010",
                "Prio_von": "B",
                "Verantwortlicher Bereich_von": "Elektronik",
                "Status Arbeitsschritt_von": "EOP",
                "Zieltermin_von": "2026-03-01",
            }
        )

        st.session_state.cpm_rows = pd.DataFrame([r1, r2])

    st.session_state.setdefault("cpm_search", "")
    st.session_state.setdefault("cpm_form_open", False)
    st.session_state.setdefault("cpm_form_mode", None)  # "new" | "edit"
    st.session_state.setdefault("selected_cpm_id", None)


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------
def _filter_df(df: pd.DataFrame, query: str) -> pd.DataFrame:
    q = (query or "").strip().lower()
    if not q:
        return df
    return df[df.apply(lambda r: q in " ".join(map(str, r.values)).lower(), axis=1)]


def _next_cpm_id() -> str:
    df = st.session_state.cpm_rows
    if df.empty:
        return "CPM-001"
    nums = []
    for x in df["CPM-ID"].astype(str).tolist():
        try:
            nums.append(int(x.split("-")[-1]))
        except Exception:
            pass
    n = max(nums) + 1 if nums else (len(df) + 1)
    return f"CPM-{n:03d}"


def _get_row_for_form(mode: str) -> dict:
    if mode == "edit" and st.session_state.selected_cpm_id:
        df = st.session_state.cpm_rows
        pick = df[df["CPM-ID"] == st.session_state.selected_cpm_id]
        if not pick.empty:
            row = pick.iloc[0].to_dict()
            if row.get("Anzeigeumfang") not in ANZEIGEUMFANG:
                row["Anzeigeumfang"] = "Nur UP-Auflösung"
            return row

    return _make_empty_row(_next_cpm_id())


def _write_row_back(mode: str, row_dict: dict):
    df = st.session_state.cpm_rows.copy()
    if mode == "new":
        st.session_state.cpm_rows = pd.concat([df, pd.DataFrame([row_dict])], ignore_index=True)
    else:
        mask = df["CPM-ID"] == row_dict["CPM-ID"]
        df.loc[mask, :] = pd.DataFrame([row_dict]).values
        st.session_state.cpm_rows = df


# ---------------------------------------------------------
# CPM Maske (Schablone) – Expander
# ---------------------------------------------------------
def _render_cpm_form(mode: str):
    row = _get_row_for_form(mode)
    cpm_id = row.get("CPM-ID", "")

    title = "CPM-Punkt neu erfassen" if mode == "new" else f"CPM bearbeiten – {cpm_id}"
    with st.expander(title, expanded=True):

        st.markdown("#### Aktionen")
        a1, a2, _ = st.columns([0.25, 0.25, 0.50])
        with a1:
            ak_cpm = st.checkbox("CPM-Punkt neu erfassen", value=bool(row.get("Aktion_CPM", False)), key=f"act_cpm_{cpm_id}")
        with a2:
            ak_sobe = st.checkbox("SOBE neu erfassen", value=bool(row.get("Aktion_SOBE", False)), key=f"act_sobe_{cpm_id}")

        st.markdown("#### Anzeigeumfang")
        # ✅ stabil: single-select Radio (horizontal)
        scope = st.radio(
            label="",
            options=ANZEIGEUMFANG,
            index=ANZEIGEUMFANG.index(row.get("Anzeigeumfang", "Nur UP-Auflösung")) if row.get("Anzeigeumfang") in ANZEIGEUMFANG else 0,
            horizontal=True,
            key=f"scope_{cpm_id}",
        )

        st.divider()
        st.markdown("#### Eingabe (von ... bis)")

        st.text_input("CPM-ID", value=cpm_id, disabled=True, key=f"id_{cpm_id}")

        form_values = {"CPM-ID": cpm_id}
        form_values["Aktion_CPM"] = bool(ak_cpm)
        form_values["Aktion_SOBE"] = bool(ak_sobe)
        form_values["Anzeigeumfang"] = scope

        for f in RANGE_FIELDS:
            c1, c2, c3 = st.columns([0.46, 0.08, 0.46])
            with c1:
                v = st.text_input(f"{f}", value=str(row.get(f"{f}_von", "")), key=f"von_{cpm_id}_{f}")
            with c2:
                st.markdown("<div style='padding-top:32px; text-align:center;'>bis</div>", unsafe_allow_html=True)
            with c3:
                b = st.text_input(" ", value=str(row.get(f"{f}_bis", "")), key=f"bis_{cpm_id}_{f}")

            form_values[f"{f}_von"] = v
            form_values[f"{f}_bis"] = b

        st.markdown("")
        csave, ccancel = st.columns([0.25, 0.25])

        with csave:
            if st.button("Speichern", use_container_width=True, key=f"save_{cpm_id}"):
                _write_row_back(mode, form_values)
                st.session_state.cpm_form_open = False
                st.session_state.cpm_form_mode = None
                st.session_state.selected_cpm_id = None
                st.rerun()

        with ccancel:
            if st.button("Abbrechen", use_container_width=True, key=f"cancel_{cpm_id}"):
                st.session_state.cpm_form_open = False
                st.session_state.cpm_form_mode = None
                st.session_state.selected_cpm_id = None
                st.rerun()


# ---------------------------------------------------------
# Page Render
# ---------------------------------------------------------
def render():
    header_bar("Classic Parts Monitor")
    _init_cpm()

    st.session_state.cpm_search = st.text_input(
        "Suche (CPM-ID / Teilenummer / Bereich / Text ...)",
        value=st.session_state.cpm_search,
        placeholder="z. B. OE3-001 oder 9A1-907-115 oder Elektronik …",
    )

    df_all = st.session_state.cpm_rows.copy()
    df = _filter_df(df_all, st.session_state.cpm_search)

    table_df = df[TABLE_COLS].copy()

    event = st.dataframe(
        table_df,
        hide_index=True,
        use_container_width=True,
        selection_mode="single-row",
        on_select="rerun",
        key="cpm_table_select",
    )

    selected_rows = []
    try:
        selected_rows = event.selection.rows
    except Exception:
        selected_rows = []

    if selected_rows:
        picked_id = table_df.iloc[selected_rows[0]]["CPM-ID"]
        st.session_state.selected_cpm_id = picked_id
        st.session_state.cpm_form_open = True
        st.session_state.cpm_form_mode = "edit"

    st.markdown("")

    if st.button("➕ CPM-Punkt neu erfassen", use_container_width=False):
        st.session_state.selected_cpm_id = None
        st.session_state.cpm_form_open = True
        st.session_state.cpm_form_mode = "new"
        st.rerun()

    if st.session_state.cpm_form_open and st.session_state.cpm_form_mode in ("new", "edit"):
        _render_cpm_form(st.session_state.cpm_form_mode)
