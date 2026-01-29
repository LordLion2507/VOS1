import os
import pandas as pd
import streamlit as st
from shared.helpers import header_bar, set_page, render_sticky_html_table

def render(aenderung_template_img_path: str):
    header_bar("Änderungsliste")

    left, mid, right = st.columns([0.22, 0.58, 0.20], gap="large")

    with left:
        st.markdown("## Aktionen")
        st.button("neues Objekt", use_container_width=True)

        st.markdown("## Objekt suchen\n")
        q = st.text_input("Suche", value=st.session_state.change_search, placeholder="z. B. OE3-001 oder Text…")
        if st.button("Suchen", use_container_width=True):
            st.session_state.change_search = q

    with mid:
        df = st.session_state.change_list
        df = df[df["ProjektNr"] == st.session_state.selected_project].copy()

        q = st.session_state.change_search.strip()
        if q:
            ql = q.lower()
            df = df[df.apply(lambda r: ql in " ".join(map(str, r.values)).lower(), axis=1)]

        if not df.empty:
            while len(df) < 14:
                df = pd.concat([df, df.iloc[[len(df) % len(df)]].copy()], ignore_index=True)

        cols = [
            "Option",
            "CPM Unterpunkt (+U?)",
            "KFMAG",
            "Beschreibung (Sonderwunsch/Baugruppe)",
            "Beispielbild",
            "Teilenummer",
            "Kategorie",
            "Regulatory evaluation",
            "DTV + Abteilung / PE",
            "K-Freigabe",
            "Qualität Norm + Abteilung",
            "Bemusterung",
            "HAL-Unterschrift",
            "QC Ersatzteil-Vorlauf",
            "Bemerkungen",
            "Wann zuletzt geändert",
        ]
        show_df = df[cols].copy()

        render_sticky_html_table(show_df, table_class="cl", sticky_col="Option", link_col="Option")
        st.caption("Hinweis: Klick-Selection wie bei st.dataframe ist hier (wegen sticky HTML) nicht aktiv – Preview bleibt Demo.")

    with right:
        st.markdown("## Weiterführend\n")
        st.button("CPM", use_container_width=True, on_click=set_page, args=("CPM",))
        st.button("Laufwerk", use_container_width=True, on_click=set_page, args=("Laufwerk",))
        st.button("Themenblätter", use_container_width=True, on_click=set_page, args=("Themenblätter",))

        st.markdown("")
        if st.session_state.change_preview_open:
            st.markdown('<div class="preview-box">', unsafe_allow_html=True)
            st.markdown('<div class="preview-title">Vorschau</div>', unsafe_allow_html=True)
            st.markdown('<div class="preview-sub">Leeres Blatt (Demo) – egal welche Option.</div>', unsafe_allow_html=True)

            if os.path.exists(aenderung_template_img_path):
                st.image(aenderung_template_img_path, use_container_width=True)
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

            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.caption("Klicke in der Tabelle → Vorschau erscheint hier.")
