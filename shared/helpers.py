import html
import pandas as pd
import streamlit as st

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
    st.markdown("### Zum Projekt")
    st.caption(f"Aktives Projekt: **{st.session_state.selected_project}**")
    st.button("Projektplan", use_container_width=True, on_click=set_page, args=("Projektplan",))
    st.button("Änderungsliste", use_container_width=True, on_click=set_page, args=("Änderungsliste",))
    st.button("Kalkulationsvorlage", use_container_width=True, on_click=set_page, args=("Kalkulationsvorlage",))
    st.button("Teams", use_container_width=True, on_click=set_page, args=("Teams",))
    st.button("Projektorganigramm", use_container_width=True, on_click=set_page, args=("Projektorganigramm",))
    st.button("LOP", use_container_width=True, on_click=set_page, args=("LOP",))
    st.button("Freigabedokumente", use_container_width=True, on_click=set_page, args=("Freigabedokumente",))

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
            "Datenablage",
            "Themenblätter",
            "Freigabedokumente",
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

def render_sticky_html_table(df: pd.DataFrame, table_class: str, sticky_col: str, link_col: str | None = None):
    cols = list(df.columns)
    thead = "<tr>" + "".join(
        [f"<th class='{'sticky' if c == sticky_col else ''}'>{html.escape(str(c))}</th>" for c in cols]
    ) + "</tr>"

    body_rows = ""
    for _, r in df.iterrows():
        tds = ""
        for c in cols:
            val = "" if pd.isna(r[c]) else str(r[c])
            cls = "sticky" if c == sticky_col else ""
            if link_col and c == link_col:
                cell = f"<span class='cl-link'>{html.escape(val)}</span>"
            else:
                cell = html.escape(val)
            tds += f"<td class='{cls}'>{cell}</td>"
        body_rows += f"<tr>{tds}</tr>"

    st.markdown(
        f"""
<div class="{table_class}-wrap">
  <table class="{table_class}-table">
    <thead>{thead}</thead>
    <tbody>{body_rows}</tbody>
  </table>
</div>
""",
        unsafe_allow_html=True,
    )
