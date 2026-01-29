import streamlit as st
from shared.helpers import header_bar

def render():
    header_bar("Teams")

    TEAMS_CHANNEL_URL = "https://porsche.sharepoint.com/sites/One-OffCustomerSonderwunsch/Shared%20Documents/Forms/AllItems.aspx?id=%2Fsites%2FOne%2DOffCustomerSonderwunsch%2FShared%20Documents%2FÜbersicht&viewid=d87398ce%2D4ca0%2D48a8%2Db7fd%2D4eb8cec2c606"

    st.markdown("### Teamskanal")

    if TEAMS_CHANNEL_URL.strip():
        st.link_button("Zum Teamskanal", TEAMS_CHANNEL_URL, use_container_width=True)
    else:
        st.warning("Bitte TEAMS_CHANNEL_URL eintragen.")
        st.button("Zum Teamskanal", use_container_width=True, disabled=True)
