import streamlit as st
import pandas as pd

# Configuración inicial del tablero
st.set_page_config(page_title="Tablero ETL", layout="wide")
st.title("📊 Tablero Interactivo - Datos ETL")

# Subir archivo Excel o CSV
archivo = st.file_uploader("📂 Cargar archivo Excel o CSV", type=["xlsx", "csv"])

if archivo is not None:
    try:
        # Leer archivo según extensión
        if archivo.name.endswith('.csv'):
            df = pd.read_csv(archivo)
        else:
            df = pd.read_excel(archivo)

        st.success("✅ Archivo cargado correctamente")

        # Vista previa
        st.subheader("👀 Vista previa de los datos")
        st.dataframe(df)

    except Exception as e:
        st.error(f"⚠️ Error al leer el archivo: {e}")
else:
    st.info("📁 Esperando que cargues un archivo Excel o CSV...")
