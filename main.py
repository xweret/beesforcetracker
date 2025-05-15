import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Bees Force - Tracker", layout="centered")

# Título principal motivacional
st.markdown("""
    <h1 style='text-align: center; color: #f9c80e;'>🐝 BEES FORCE · CREACIÓN DE VALOR 🚀</h1>
""", unsafe_allow_html=True)

st.subheader("Cargá y seguí el progreso de tus SKUs en puntos de venta")

# Supervisores y sus promotores
supervisores = {
    "FEDERICO SUAREZ": [
        "ALEJANDRA CAMARA", "MARCELO RIOS", "LUCIANO PEREZ", "BRAIAN ABREGU",
        "ALEX KOLLETH", "NAHUEL MACIEL", "DAIANA MAIDA", "MATIAS RIVAROLA"
    ],
    "LEONARDO FERRO": [
        "KAREN CORREA", "LUCAS FERNANDEZ", "JUAN FLOCCO", "DIEGO MARIOTTO",
        "LAURA DOMINGUEZ", "CECILIA CAPONINI", "AGOSTINA BARBERIS", "FACUNDO ALBANESI"
    ]
}

# Cargar base de datos local o crear una nueva
@st.cache_data
def load_data():
    try:
        return pd.read_csv("skus_data.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["Fecha", "Supervisor", "Promotor", "SKU", "Punto de Venta"])

data = load_data()

# Formulario de carga
with st.form("formulario_sku"):
    st.markdown("### 📝 Registrar nuevo SKU")
    col1, col2 = st.columns(2)
    with col1:
        supervisor = st.selectbox("Supervisor", list(supervisores.keys()), key="supervisor")
    with col2:
        promotor = st.selectbox("Promotor", supervisores[supervisor], key="promotor")
    
    sku = st.text_input("SKU")
    punto = st.text_input("Punto de Venta")
    submitted = st.form_submit_button("Registrar")

    if submitted and sku and punto:
        nueva_fila = {
            "Fecha": datetime.date.today(),
            "Supervisor": supervisor,
            "Promotor": promotor,
            "SKU": sku,
            "Punto de Venta": punto
        }
        data = pd.concat([data, pd.DataFrame([nueva_fila])], ignore_index=True)
        data.to_csv("skus_data.csv", index=False)
        st.success(f"🎉 ¡SKU registrado exitosamente para {promotor}!")
        st.balloons()

# Visualización de progreso
st.markdown("### 📈 Progreso por Supervisor")

if not data.empty:
    for sup, lista_promos in supervisores.items():
        subset = data[data["Supervisor"] == sup]
        total = len(subset)
        st.markdown(f"#### 🧑‍💼 {sup} — {total} SKUs")
        st.progress(min(total / 50, 1.0))

        for prom in lista_promos:
            count = len(subset[subset["Promotor"] == prom])
            st.text(f"{prom} — {count} SKUs")
            st.progress(min(count / 20, 1.0))
else:
    st.info("No hay datos cargados todavía.")

# Ver tabla de datos completa
with st.expander("📄 Ver registros completos"):
    st.dataframe(data)
