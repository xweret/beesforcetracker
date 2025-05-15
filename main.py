import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Bees Porce Tracker", layout="centered")

st.title("🚀 Tracker de Valor - Bees Porce")
st.subheader("Seguimiento de SKUs en Puntos de Venta")

# Cargar o crear base de datos local
@st.cache_data
def load_data():
    try:
        return pd.read_csv("skus_data.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["Fecha", "Promotor", "SKU", "Punto de Venta"])

data = load_data()

# Formulario de carga
with st.form("formulario_sku"):
    st.markdown("### 📥 Registrar nuevo SKU")
    promotor = st.text_input("Nombre del promotor")
    sku = st.text_input("SKU")
    punto = st.text_input("Punto de Venta")
    submitted = st.form_submit_button("Registrar")
    if submitted and promotor and sku and punto:
        nueva_fila = {
            "Fecha": datetime.date.today(),
            "Promotor": promotor,
            "SKU": sku,
            "Punto de Venta": punto
        }
        data = pd.concat([data, pd.DataFrame([nueva_fila])], ignore_index=True)
        data.to_csv("skus_data.csv", index=False)
        st.success("✅ SKU registrado exitosamente!")

# Visualización por promotor
st.markdown("### 📊 Progreso por Promotor")
if not data.empty:
    progreso = data.groupby("Promotor").count()["SKU"].reset_index()
    progreso = progreso.rename(columns={"SKU": "Total SKUs"})

    for _, row in progreso.iterrows():
        st.markdown(f"**{row['Promotor']}**")
        st.progress(min(row["Total SKUs"]/20, 1.0), text=f"{row['Total SKUs']} SKUs")  # max 20 como ejemplo

else:
    st.info("Aún no hay registros. Comenzá cargando un SKU arriba.")

# Mostrar tabla (opcional)
with st.expander("📄 Ver todos los registros"):
    st.dataframe(data)
