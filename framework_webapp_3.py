import streamlit as st
import pandas as pd

# Titolo della webapp
st.set_page_config(page_title="Project Framework Viewer", layout="wide")
st.title("📊 Project Framework WebApp")

# Caricamento del file Excel
excel_file = "Draft Framework.xlsx"

# Lettura dei fogli
df_framework = pd.read_excel(excel_file, sheet_name="Foglio1", engine="openpyxl")
df_roles = pd.read_excel(excel_file, sheet_name="Foglio2", engine="openpyxl")

# Pulizia dei dati
df_framework.columns = df_framework.columns.str.strip()
df_roles.columns = df_roles.columns.str.strip()

# Selezione Macro-phase e Phase
macro_phases = df_framework["Macro-phase"].dropna().unique()
selected_macro = st.selectbox("Seleziona una Macro-phase", macro_phases)

phases = df_framework[df_framework["Macro-phase"] == selected_macro]["Phase"].dropna().unique()
selected_phase = st.selectbox("Seleziona una Phase", phases)

# Filtraggio dei dati
filtered_df = df_framework[
    (df_framework["Macro-phase"] == selected_macro) &
    (df_framework["Phase"] == selected_phase)
]

# Tabs per Deliverables, People, Tools, KPI
tab1, tab2, tab3, tab4 = st.tabs(["📦 Deliverables", "👥 People Involvement", "🛠️ Tools", "📈 KPI"])

with tab1:
    st.subheader("Deliverables")
    st.dataframe(filtered_df[["Sub-phase", "Deliverables"]].dropna(how="all"))

with tab2:
    st.subheader("People Involvement")
    st.write("Responsabili e Accountable per ciascuna sottofase:")
    st.dataframe(filtered_df[["Sub-phase", "Responsibile Roles", "Accountable Roles"]].dropna(how="all"))
    st.write("📋 Mappatura Ruoli → Persone:")
    st.dataframe(df_roles)

with tab3:
    st.subheader("Tools")
    st.info("Puoi usare questo spazio per annotare gli strumenti utilizzati per ogni sottofase.")
    for i, row in filtered_df.iterrows():
        st.text_input(f"Tools per '{row['Sub-phase']}'", key=f"tools_{i}")

with tab4:
    st.subheader("KPI")
    st.info("Puoi usare questo spazio per annotare i KPI associati a ciascuna sottofase.")
    for i, row in filtered_df.iterrows():
        st.text_input(f"KPI per '{row['Sub-phase']}'", key=f"kpi_{i}")
