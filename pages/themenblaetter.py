import pandas as pd
import streamlit as st
from datetime import date
from shared.helpers import header_bar

def render():
    header_bar("Themenblatt Details")

    left, mid, right = st.columns([0.22, 0.33, 0.45], gap="large")

    with left:
        if st.button("Neues Themenblatt", use_container_width=True):
            st.session_state.selected_topic_id = "__NEW__"

        st.markdown("#### Themenblätter suchen")
        search_key = st.text_input("Suche", value=st.session_state.topic_search, placeholder="TB-014 oder Begriff…")
        if st.button("Suchen", use_container_width=True):
            st.session_state.topic_search = search_key

    with mid:
        st.markdown("<div class='topic-list-title'>Deine Themenblätter</div>", unsafe_allow_html=True)

        df = st.session_state.topics
        df = df[(df["ProjektNr"] == st.session_state.selected_project) & (df["Owner"] == "Du")].copy()

        key = st.session_state.topic_search.strip()
        if key:
            kl = key.lower()
            df = df[df["ThemenblattID"].str.lower().str.contains(kl) | df["Titel"].str.lower().str.contains(kl)]

        if not df.empty:
            while len(df) < 10:
                df = pd.concat([df, df.iloc[[len(df) % len(df)]].copy()], ignore_index=True)

        if df.empty:
            st.caption("Keine Themenblätter gefunden.")
        else:
            for i, row in df.iterrows():
                label = f'{row["ThemenblattID"]} – {row["Titel"]}'
                if st.button(label, use_container_width=True, key=f"tb_{row['ThemenblattID']}_{i}"):
                    st.session_state.selected_topic_id = row["ThemenblattID"]

    with right:
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
                st.info("Bitte ein Themenblatt auswählen.")
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
                        st.rerun()

                st.divider()
                st.markdown("**Beschreibung**")
                st.write(row["Beschreibung"])
