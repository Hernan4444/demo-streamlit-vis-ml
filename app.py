import altair as alt
import streamlit as st
import pandas as pd
import folium
from folium.plugins import FastMarkerCluster
from streamlit_folium import st_folium
from ml import load_pipeline, ml_zone
from utils.utils import number_to_text
from dotenv import load_dotenv
import zipfile
import os


@st.cache_data
def load_data(zip_filename, csv_filename):
    print("Cargando datos")
    # Obtener contraseña
    load_dotenv()
    zip_password = os.getenv("CSV_PASSWORD")

    # Leer el CSV desde el ZIP con contraseña
    with zipfile.ZipFile(zip_filename) as zf:
        with zf.open(csv_filename, pwd=zip_password.encode()) as f:
            df = pd.read_csv(f)

    # Procesar el DataFrame
    df.es_superhost = df.es_superhost.map(number_to_text)
    df.servicio_aire_acondicionado = df.servicio_aire_acondicionado.map(number_to_text)
    return df


def add_title_and_description():
    """
    Añadir textos iniciales a la demo
    """
    st.title("Airbnb Demo")
    st.write("Este _dashboard_ muestra información sobre diferentes Airbnb en 10 ciudades.")


def show_airbnb_dataframe(df):
    """
    Mostrar dataframe
    """
    opciones_paises = ["Todos los Países"] + list(df["pais"].unique())
    option_box = st.selectbox("Selecciona un pais", opciones_paises)
    capacidad_slider = st.slider("Capacidad", min_value=0, max_value=17, value=2, step=1)

    filtered_df = df[df.capacidad >= capacidad_slider]
    if option_box and option_box != "Todos los Países":
        filtered_df = filtered_df[filtered_df["pais"] == option_box]

    st.write(filtered_df)
    return filtered_df


def show_airbnb_in_map(df):
    """
    Mapa de los airbnb.
    Si hay más de un país, muestra un ClusterMap
    En caso contrario, muestra un mapa simple de puntos
    """
    positions = df[["latitud", "longitud"]]
    if df.pais.nunique() > 1:
        st.subheader(f"ClusterMap de Airbnb")
        center = [positions.latitud.mean(), positions.longitud.mean()]
        f_map = folium.Map()

        # Extra: Cuando usamos folium necesitamos
        # restrigir el tamaño con CSS por un bug que todavía no corrigen
        st.markdown(
            "<style>iframe[title='streamlit_folium.st_folium'] {height: 500px;}</style>",
            unsafe_allow_html=True,
        )

        st_folium(
            f_map,
            feature_group_to_add=[FastMarkerCluster(positions)],
            center=center,
            zoom=2,
            width=1200,
            height=500,
            use_container_width=True,
            returned_objects=[],
        )
    else:
        pais = df["pais"].unique()[0]
        st.subheader(f"Airbnb en - {pais}")
        st.map(data=positions, latitude="latitud", longitude="longitud")


def plot_days_of_week(df, column):
    """
    Visualizaciones con altair
    """
    column.subheader("Anfitriones por tiempo de respuesta")

    grupo_contado = (
        df.groupby("tiempo_respuesta")["anfitrión/a"]
        .nunique()  # Cuantos datos hay sin considerar repetidos
        .reset_index(name="Cantidad")
    )

    tiempo_respuesta = (
        alt.Chart(grupo_contado)
        .mark_bar()
        .encode(
            x="Cantidad",
            y=alt.Y("tiempo_respuesta:N", axis=alt.Axis(labelLimit=200)),
        )
    ).properties(height=300)

    column.altair_chart(tiempo_respuesta, use_container_width=True)


def plot_airbnb_by_superhost(df, column):
    """
    Visualizaciones con altair
    """
    column.subheader("Airbnb por superhost")
    pie = (
        alt.Chart(df)
        .mark_arc()
        .encode(
            theta="count()",
            color=alt.Color("es_superhost:N", scale=alt.Scale(scheme="set2")),
        )
    ).properties(height=300, width=350)

    column.altair_chart(pie)


def interactive_view(df):
    """
    Visualizaciones interactivas con altair
    """
    st.subheader("Propiedad y servicio de aire acondicionado")
    selection = alt.selection_point(fields=["servicio_aire_acondicionado"], bind="legend")

    pie = (
        alt.Chart(df)
        .mark_arc()
        .encode(
            theta="count()",
            color=alt.Color(
                "servicio_aire_acondicionado:N",
                legend=alt.Legend(title="Aire"),
                scale=alt.Scale(scheme="set2"),
            ),
            opacity=alt.condition(selection, alt.value(1), alt.value(0.2)),
        )
        .add_params(selection)
        .properties(width=200)
    )

    bar = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x="count()",
            y=alt.Y("tipo_propiedad:N", axis=alt.Axis(labelLimit=200)),
        )
        .add_params(selection)
        .transform_filter(selection)
        .properties(height=300, width=200)
    )
    juntos = bar | pie
    st.altair_chart(juntos)


if __name__ == "__main__":
    print("Cargando streamlit")
    df = load_data("Airbnb_Locations.zip", "Airbnb_Locations.csv")

    # Textos y filtros
    add_title_and_description()
    filtered_df = show_airbnb_dataframe(df)

    # Gráficos
    show_airbnb_in_map(filtered_df)
    column_1, column_2 = st.columns(2)
    plot_days_of_week(filtered_df, column_1)
    plot_airbnb_by_superhost(filtered_df, column_2)
    interactive_view(filtered_df)

    # Parte ML
    pipeline = load_pipeline()
    ml_zone(pipeline)
