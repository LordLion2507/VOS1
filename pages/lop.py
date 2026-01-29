import html
import pandas as pd
import streamlit as st
from shared.helpers import header_bar

def _render_lop_table(df: pd.DataFrame):
    cols = list(df.columns)
    sticky_col = cols[0] if cols else None

    thead = "<tr>" + "".join(
        [f"<th class='{'sticky' if c == sticky_col else ''}'>{html.escape(c)}</th>" for c in cols]
    ) + "</tr>"

    body_rows = ""
    for _, r in df.iterrows():
        tds = ""
        for c in cols:
            val = "" if pd.isna(r[c]) else str(r[c])
            cls = "sticky" if c == sticky_col else ""
            tds += f"<td class='{cls}'>{html.escape(val)}</td>"
        body_rows += f"<tr>{tds}</tr>"

    st.markdown(
        f"""
<div class="lop-shell">
  <div class="lop-toolbar" title="Tabelle-Tools (Demo)">
    <span class="lop-tool" title="Spalten auswählen">⚙️</span>
    <span class="lop-tool" title="Download">⬇️</span>
    <span class="lop-tool" title="Suche">🔍</span>
    <span class="lop-tool" title="Vollbild">⛶</span>
  </div>

  <div class="lop-wrap">
    <table class="lop-table">
      <thead>{thead}</thead>
      <tbody>{body_rows}</tbody>
    </table>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

def render():
    header_bar("LOP")
    df = st.session_state.lop.copy()
    while len(df) < 10:
        df = pd.concat([df, df.iloc[[len(df) % 3]].copy()], ignore_index=True)
    _render_lop_table(df)
