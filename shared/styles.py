import streamlit as st

def inject_global_css():
    st.markdown(
        """
<style>
.block-container { padding-top: 1.2rem; padding-bottom: 2rem; }

a.demo-link {
  color: #1a73e8;
  text-decoration: underline;
  cursor: pointer;
}

.demo-card {
  border: 1px solid #E6E6E6;
  border-radius: 10px;
  padding: 14px 14px;
  background: #FFFFFF;
}

.sidebar-card {
  border: 1px solid #EAEAEA;
  border-radius: 10px;
  padding: 12px;
  background: #FAFAFA;
}

/* LOP: horizontal scroll + sticky first column */
.lop-wrap { overflow-x: auto; border: 1px solid #E6E6E6; border-radius: 10px; }
.lop-table { border-collapse: collapse; width: 1600px; }
.lop-table th, .lop-table td { border: 1px solid #E6E6E6; padding: 10px; font-size: 14px; white-space: nowrap; }
.lop-table th { background: #F5F5F5; font-weight: 600; position: sticky; top: 0; z-index: 3; }
.lop-table td.sticky, .lop-table th.sticky { position: sticky; left: 0; background: #FFFFFF; z-index: 4; }
.lop-table th.sticky { background: #F5F5F5; }

/* Änderungsliste Preview rechts unten */
.preview-box {
  border: 1px solid #E6E6E6;
  border-radius: 10px;
  background: #FFFFFF;
  height: 520px;
  padding: 10px;
}
.preview-title { font-weight: 700; margin-bottom: 6px; }
.preview-sub { color: #666; font-size: 13px; margin-bottom: 10px; }

/* Laufwerk */
.drive-item {
  padding: 10px 12px;
  border: 1px solid #E6E6E6;
  border-radius: 10px;
  margin-bottom: 8px;
  background: #FFFFFF;
}
.drive-title { font-weight: 650; }
.drive-meta { color:#666; font-size: 12px; }

/* Sticky HTML Table (für Änderungsliste) */
.cl-wrap { overflow-x: auto; border: 1px solid #E6E6E6; border-radius: 10px; background:#fff; }
.cl-table { border-collapse: collapse; width: 2100px; }
.cl-table th, .cl-table td { border: 1px solid #E6E6E6; padding: 10px; font-size: 14px; white-space: nowrap; }
.cl-table th { background: #F5F5F5; font-weight: 600; position: sticky; top: 0; z-index: 3; }
.cl-table td.sticky, .cl-table th.sticky { position: sticky; left: 0; background: #FFFFFF; z-index: 4; }
.cl-table th.sticky { background: #F5F5F5; }
.cl-link { color:#1a73e8; text-decoration: underline; font-weight: 500; cursor:pointer; }

/* LOP: Hover-Toolbar oben rechts */
.lop-shell { position: relative; }
.lop-toolbar {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(245,245,245,0.95);
  border: 1px solid #E6E6E6;
  border-radius: 8px;
  padding: 6px 8px;
  display: flex;
  gap: 10px;
  opacity: 0;
  transition: opacity .15s ease-in-out;
  z-index: 10;
}
.lop-shell:hover .lop-toolbar { opacity: 1; }
.lop-tool { font-size: 16px; color:#444; user-select:none; }
.lop-tool:hover { color:#111; }

/* Laufwerk: Button wie List-Item */
.drive-btn > button {
  width: 100%;
  text-align: left !important;
  border: 1px solid #E6E6E6 !important;
  border-radius: 10px !important;
  padding: 12px 12px !important;
  background: #FFFFFF !important;
}
.drive-btn > button:hover { border-color:#D0D0D0 !important; }
.drive-btn-label { font-weight: 650; display:block; }
.drive-btn-meta { color:#666; font-size:12px; display:block; margin-top:2px; }

/* Themenblätter: größere rechte Liste */
.topic-list-title { font-size: 22px; font-weight: 800; margin-bottom: 10px; }
</style>
""",
        unsafe_allow_html=True,
    )
