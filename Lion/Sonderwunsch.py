import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # Repo-Root
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import os
import streamlit as st

from shared.styles import inject_global_css
from shared.data import seed_data
from shared.helpers import sidebar_global

from pages import (
    laufwerk,
    projektuebersicht,
    projektplan,
    aenderungsliste,
    kalkulationsvorlage,
    teams,
    projektorganigramm,
    lop,
    cpm,
    themenblaetter,
    freigabedokumente,
)

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
inject_global_css()

# ---------------------------------------------------------
# SESSION STATE INIT
# ---------------------------------------------------------
if "data_initialized" not in st.session_state:
    (
        st.session_state.projects,
        st.session_state.change_list,
        st.session_state.topics,
        st.session_state.lop,
        st.session_state.drive_tree,
    ) = seed_data()
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
# ROUTER
# ---------------------------------------------------------
sidebar_global()
page = st.session_state.page

if page == "Projektübersicht":
    projektuebersicht.render()
elif page == "Projektplan":
    projektplan.render(PROJECTPLAN_IMG)
elif page == "Änderungsliste":
    aenderungsliste.render(AENDERUNG_TEMPLATE_IMG)
elif page == "Kalkulationsvorlage":
    kalkulationsvorlage.render()
elif page == "Teams":
    teams.render()
elif page == "Projektorganigramm":
    projektorganigramm.render()
elif page == "LOP":
    lop.render()
elif page == "CPM":
    cpm.render()
elif page == "Laufwerk":
    laufwerk.render()
elif page == "Themenblätter":
    themenblaetter.render()
elif page == "Freigabedokumente":
    freigabedokumente.render()
else:
    projektuebersicht.render()


# Zum Starten:
# python3 -m streamlit run "/Users/U6TI4RR/VOS1 Demo/Lion/Sonderwunsch.py"
