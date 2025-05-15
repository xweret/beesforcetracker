import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Bees Porce Tracker", layout="centered")

st.title("🧬 Tracker de Valor - Bees Porce")
st.subheader("Cargá y seguí el progreso de tus SKUs")

# Supervisores y vendedores
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

@st.cache_data
def load_data():
    try:
        return pd.read_csv("skus_data.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["Fecha", "Supervisor", "Promotor", "SKU", "Punto de Venta"])

data = load_data()

with st.form("formulario"):
    st.markdown("### 📝 Cargar nuevo SKU")
    supervisor = st.selectbox("Supervisor", list(supervisores.keys()))
    promotor = st.selectbox("Promotor", supervisores[supervisor])
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
        st.success("✅ SKU registrado correctamente!")

# Visualización del progreso
st.markdown("### 📈 Progreso por Supervisor")

if not data.empty:
    for sup in supervisores.keys():
        subset = data[data["Supervisor"] == sup]
        total = len(subset)
        st.markdown(f"#### 🧑‍💼 {sup} — {total} SKUs")
        st.progress(min(total / 50, 1.0))

        for prom in supervisores[sup]:
            count = len(subset[subset["Promotor"] == prom])
            st.text(f"{prom} — {count} SKUs")
            st.progress(min(count / 20, 1.0))
else:
    st.info("No hay datos aún. Cargá tu primer SKU arriba.")

# Tabla opcional
with st.expander("📄 Ver registros"):
    st.dataframe(data)
