import pandas as pd
import streamlit as st
from datetime import date
from shared.helpers import header_bar

def render():
    header_bar("Freigabedokumente")

    if "release_docs" not in st.session_state:
        st.session_state.release_docs = [
            {"Name": "B-Freigabe – OE3-001 – Gesamtfahrzeug.pdf", "Typ": "B-Freigabe", "Stand": "2026-01-18"},
            {"Name": "K-Freigabe – OE3-002 – Konstruktion.pdf", "Typ": "K-Freigabe", "Stand": "2026-01-22"},
            {"Name": "B-Freigabe – OE3-003 – Zulassung.pdf", "Typ": "B-Freigabe", "Stand": "2026-01-20"},
            {"Name": "K-Freigabe – OE3-007 – Elektronik.pdf", "Typ": "K-Freigabe", "Stand": "2026-01-24"},
        ]

    st.session_state.setdefault("selected_release_doc", None)

    left, right = st.columns([0.60, 0.40], gap="large")

    with left:
        st.markdown("### Dokumente")
        df = pd.DataFrame(st.session_state.release_docs)
        st.dataframe(df, use_container_width=True, hide_index=True, height=360)

        names = [d["Name"] for d in st.session_state.release_docs]
        options = ["— bitte auswählen —"] + names

        current = st.session_state.get("selected_release_doc")
        if current not in options:
            current = "— bitte auswählen —"
            st.session_state.selected_release_doc = current

        st.session_state.selected_release_doc = st.selectbox(
            "Dokument auswählen",
            options=options,
            index=options.index(current),
        )

        if st.session_state.selected_release_doc != "— bitte auswählen —":
            dummy_bytes = (f"Demo-Freigabedokument: {st.session_state.selected_release_doc}\n").encode("utf-8")
            st.download_button(
                "Ausgewähltes Dokument herunterladen",
                data=dummy_bytes,
                file_name=st.session_state.selected_release_doc.replace(" ", "_"),
                mime="application/pdf",
                use_container_width=True,
            )

    with right:
        st.markdown("### Upload (Drag & Drop)")
        up = st.file_uploader(
            "Freigabedokument hochladen",
            type=["pdf", "xlsx", "docx", "png", "jpg"],
            accept_multiple_files=False,
            label_visibility="collapsed",
        )

        if up is not None:
            st.success(f"Hochgeladen (Demo): {up.name}")
            st.session_state.release_docs.insert(0, {"Name": up.name, "Typ": "—", "Stand": str(date.today())})

        st.caption("Hinweis: In der echten Version würdest du hier nach SharePoint/Backend schreiben.")
