import streamlit as st
from shared.helpers import header_bar

def render():
    header_bar("Laufwerk")

    if len(st.session_state.drive_path) > 0:
        if st.button("Back", use_container_width=False):
            st.session_state.drive_path.pop()
            st.rerun()

    node = st.session_state.drive_tree
    for p in st.session_state.drive_path:
        node = node.get(p, {})

    if not node:
        st.caption("Hier würden Dateien/Links erscheinen. Für die Demo reicht 'leer' + Navigation.")
    else:
        for folder in node.keys():
            clicked = st.button(
                f"✿  {folder}\n",
                key=f"folder_{'/'.join(st.session_state.drive_path)}_{folder}",
                use_container_width=True,
            )
            st.markdown("<span class='drive-btn-meta'>Dateiordner</span>", unsafe_allow_html=True)

            if clicked:
                st.session_state.drive_path.append(folder)
                st.rerun()
