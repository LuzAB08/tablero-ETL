import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración inicial del tablero
st.set_page_config(page_title="Tablero ETL", layout="wide")
st.title("\ud83d\udcca Tablero Interactivo - Datos ETL")

# Subida del archivo
archivo = st.file_uploader("\ud83d\udcc2 Cargar archivo Excel o CSV", type=["xlsx", "csv"])

if archivo is not None:
    try:
        # Leer archivo según extensión
        if archivo.name.endswith('.csv'):
            df = pd.read_csv(archivo)
        else:
            df = pd.read_excel(archivo)

        st.success("\u2705 Archivo cargado correctamente")

        # Filtros en la barra lateral
        st.sidebar.header("\ud83d\udd39 Filtros")

        marcas = st.sidebar.multiselect("Marca", options=df["Marca"].dropna().unique())
        zonas = st.sidebar.multiselect("Zona", options=df["Zona"].dropna().unique())
        rutas = st.sidebar.multiselect("Ruta", options=df["Ruta"].dropna().unique())

        fecha_min = pd.to_datetime(df["Fecha de Varada"], errors='coerce').min()
        fecha_max = pd.to_datetime(df["Fecha de Varada"], errors='coerce').max()

        fecha_inicio, fecha_fin = st.sidebar.date_input("Rango de Fecha de Varada", [fecha_min, fecha_max])

        edad_min, edad_max = int(df["Edad"].min()), int(df["Edad"].max())
        edad_rango = st.sidebar.slider("Edad del vehículo", edad_min, edad_max, (edad_min, edad_max))

        # Aplicar filtros
        df["Fecha de Varada"] = pd.to_datetime(df["Fecha de Varada"], errors='coerce')
        df_filtrado = df[
            (df["Fecha de Varada"] >= pd.to_datetime(fecha_inicio)) &
            (df["Fecha de Varada"] <= pd.to_datetime(fecha_fin)) &
            (df["Edad"] >= edad_rango[0]) & (df["Edad"] <= edad_rango[1])
        ]

        if marcas:
            df_filtrado = df_filtrado[df_filtrado["Marca"].isin(marcas)]
        if zonas:
            df_filtrado = df_filtrado[df_filtrado["Zona"].isin(zonas)]
        if rutas:
            df_filtrado = df_filtrado[df_filtrado["Ruta"].isin(rutas)]

        st.subheader("\ud83d\udd22 Vista Previa de Datos Filtrados")
        st.dataframe(df_filtrado)

        st.markdown("---")
        
        # Visualizaciones
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("\ud83d\udcc5 Varadas por Marca")
            fig_marca = px.histogram(df_filtrado, x="Marca", title="Cantidad de Varadas por Marca")
            st.plotly_chart(fig_marca, use_container_width=True)

        with col2:
            st.subheader("\ud83c\udf0d Varadas por Zona")
            fig_zona = px.histogram(df_filtrado, x="Zona", title="Cantidad de Varadas por Zona")
            st.plotly_chart(fig_zona, use_container_width=True)

        st.subheader("\ud83d\udcc6 Varadas por Día")
        varadas_diarias = df_filtrado.groupby("Fecha de Varada").size().reset_index(name="Cantidad")
        fig_line = px.line(varadas_diarias, x="Fecha de Varada", y="Cantidad", title="Varadas por Fecha")
        st.plotly_chart(fig_line, use_container_width=True)

        st.subheader("\u23f1\ufe0f Tiempo de Habilitación")
        fig_hist = px.histogram(df_filtrado, x="Tiempo habilitación", nbins=30, title="Distribución del Tiempo de Habilitación")
        st.plotly_chart(fig_hist, use_container_width=True)

    except Exception as e:
        st.error(f"\u26a0\ufe0f Error al procesar el archivo: {e}")
else:
    st.info("\ud83d\udcc1 Esperando que cargues un archivo Excel o CSV...")
