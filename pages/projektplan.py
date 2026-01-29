import os
import streamlit as st
from shared.helpers import header_bar

def render(projectplan_img_path: str):
    header_bar("Projektplan")

    if os.path.exists(projectplan_img_path):
        st.image(projectplan_img_path, use_container_width=True)
    else:
        st.warning(f"Lege ein Bild unter **{projectplan_img_path}** ab (Ordner `assets/`), dann wird es hier angezeigt.")
