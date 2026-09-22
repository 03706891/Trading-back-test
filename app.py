import streamlit as st
import pandas as pd

st.set_page_config(page_title="PDR Trading Backtest", layout="centered")

st.title("🪶 Data Collection & Prediction")

uploaded_file = st.sidebar.file_uploader("Încarcă datele tale (2016-2025)", type=["csv", "json"])

if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_json(uploaded_file)
    
    st.sidebar.success(f"Încărcat cu succes: {len(df)} înregistrări")

    st.sidebar.header("Filtre")
    
    start_opts = ["ALL"] + list(df['start'].unique()) if 'start' in df.columns else ["ALL"]
    color_opts = ["ALL"] + list(df['color'].unique()) if 'color' in df.columns else ["ALL"]
    pos_opts = ["ALL"] + list(df['position'].unique()) if 'position' in df.columns else ["ALL"]
    sess_opts = ["ALL"] + list(df['session'].unique()) if 'session' in df.columns else ["ALL"]
    tf_opts = ["ALL"] + list(df['tf'].unique()) if 'tf' in df.columns else ["ALL"]

    s_val = st.sidebar.selectbox("Start:", start_opts)
    c_val = st.sidebar.selectbox("Color:", color_opts)
    p_val = st.sidebar.selectbox("Position:", pos_opts)
    ss_val = st.sidebar.selectbox("Session:", sess_opts)
    tf_val = st.sidebar.selectbox("ODR T/F:", tf_opts)

    incl_session = st.sidebar.checkbox("Outcome : Incl. Session", value=True)

    filtered = df.copy()
    if s_val != "ALL": filtered = filtered[filtered['start'] == s_val]
    if c_val != "ALL": filtered = filtered[filtered['color'] == c_val]
    if p_val != "ALL": filtered = filtered[filtered['position'] == p_val]
    if ss_val != "ALL": filtered = filtered[filtered['session'] == ss_val]
    if tf_val != "ALL": filtered = filtered[filtered['tf'] == tf_val]

    total = len(filtered)
    st.subheader("All Most Likely Outcomes:")

    if total == 0:
        st.warning("Nu există date colectate pentru această combinație exactă.")
    else:
        group_cols = ['outcomeZone', 'outcomeColor']
        if incl_session and 'outcomeSession' in filtered.columns:
            group_cols.append('outcomeSession')
            
        res = filtered.groupby(group_cols).size().reset_index(name='Count')
        res['Procent (%)'] = ((res['Count'] / total) * 100).round(2)
        res = res.sort_values(by='Count', ascending=False)
        
        st.dataframe(res, use_container_width=True)

else:
    st.info("Te rugăm să încarci fișierul tău cu date (CSV sau JSON) din meniul din stânga pentru a începe.")
