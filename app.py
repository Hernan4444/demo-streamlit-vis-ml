import altair as alt
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from folium.plugins import FastMarkerCluster
from streamlit_folium import st_folium
from ml import load_pipeline, ml_zone
from utils.utils import number_to_text
from dotenv import load_dotenv
import zipfile
import os


# Usar cache_data para que esta función solo se ejecute 1 vez
# y no cada vez que se recarga la página
@st.cache_data
def load_data(zip_filename, csv_filename):
    print("Cargando datos")
    # Obtener contraseña
    load_dotenv()
    zip_password = os.getenv("CSV_PASSWORD")

    # Leer el CSV desde el ZIP con contraseña
    with zipfile.ZipFile(zip_filename) as zf:
        with zf.open(csv_filename, pwd=zip_password.encode("UTF-8")) as f:
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
    Incluir 2 filtros: Paises y Capacidad
    - Países: selectbox con todos los países o "Todos los Países"
    - Capacidad: slider con valores entre 1 y 16 (valor mínimo y máximo de la columna capacidad)
    """
    opciones_paises = ["Todos los Países"] + list(df["pais"].unique())
    min_value_capacidad = df["capacidad"].min()
    max_value_capacidad = df["capacidad"].max()

    option_box = st.selectbox("Selecciona un pais", opciones_paises)
    capacidad_slider = st.slider(
        "Capacidad", min_value=min_value_capacidad, max_value=max_value_capacidad, 
        value=min_value_capacidad, step=1
    )

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
        st.subheader("ClusterMap de Airbnb")
        center = [positions.latitud.mean(), positions.longitud.mean()]
        f_map = folium.Map()

        # Extra: Cuando usamos folium necesitamos
        # restrigir el tamaño con CSS por un bug que todavía no corrigen
        st.markdown(
            "<style>iframe[title='streamlit_folium.st_folium'] {height: 500px;}</style>",
            unsafe_allow_html=True,
        )

        # returned_objects=[] es para que Streamlit no recargue la página cada vez
        # que hacemos zoom o movemos el mapa.
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
        pais_seleccionado = df["pais"].unique()[0]
        st.subheader(f"Airbnb en - {pais_seleccionado}")
        st.map(data=positions, latitude="latitud", longitude="longitud")


def plot_by_response_time_seaborn(df):
    """
    Visualizaciones con Seaborn
    """
    # 2 columnas donde la segunda es más ancha que la primera
    st.subheader("Anfitriones por tiempo de respuesta")
    column_1, column_2 = st.columns((2, 3))
    column_1.write("DataFrame de Pandas")
    column_2.write("Visualización con Seaborn")

    # Eliminar filas con anfitrión duplicado
    df_sin_duplicados = df.drop_duplicates(subset=["anfitrión/a"])

    # Agrupar dataset por anfitrión y contar
    df_agrupado = df_sin_duplicados.groupby("tiempo_respuesta").size()
    df_agrupado = df_agrupado.reset_index(name="Cantidad").set_index("tiempo_respuesta")

    # Incluir el DataFrame en la primera columna
    column_1.write(df_agrupado)

    # Visualización con Seaborn en la segunda columna
    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots()
    sns.barplot(y="tiempo_respuesta", x="Cantidad", data=df_agrupado, ax=ax)
    ax.set_title("Cantidad de anfitriones por tiempo de respuesta")
    ax.set_ylabel("Tiempo de respuesta")
    ax.set_xlabel("Cantidad de anfitriones")
    column_2.pyplot(fig)


def interactive_view_altair(df):
    """
    Visualizaciones interactivas con Altair
    """
    st.subheader("Propiedad y servicio de aire acondicionado")
    st.write("Puedes presionar la leyenda del _pie chart_ para filtrar los datos.")

    # Crear objeto de selección para el aire acondicionado
    selection = alt.selection_point(fields=["servicio_aire_acondicionado"], bind="legend")

    # Definir como se va a codificar el color en Altair
    color_altair = alt.Color(
        "servicio_aire_acondicionado:N",
        legend=alt.Legend(title="Aire Acondicionado"),
        scale=alt.Scale(scheme="set2"),
    )

    # El gráfico de pastel muestra la proporción entre Airbnb con y sin aire acondicionado
    # Agregamos el selector para que al hacer click en la leyenda se resalte una categoría.
    pie = (
        alt.Chart(df)
        .mark_arc()
        .encode(
            theta="count()",
            color=color_altair,
            opacity=alt.condition(selection, alt.value(1), alt.value(0.2)),
        )
        .add_params(selection)
        .properties(width=200)
    )

    # El gráfico de barras apilado muestra la cantidad de Airbnb por tipo de propiedad
    # el color se usa para distinguir entre los que tienen y no tienen aire acondicionado
    # Agregamos el selector para que al hacer click en la leyenda se filtre el gráfico.
    bar = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X("count()", axis=alt.Axis(title="Cantidad de Airbnb")),
            y=alt.Y("tipo_propiedad:N", axis=alt.Axis(labelLimit=200), title="Tipo de Propiedad"),
            color=color_altair,
        )
        .add_params(selection)
        .transform_filter(selection)
        .properties(height=300, width=200)
    )

    # Unir los gráficos de barras y pastel en una sola visualización
    juntos = bar | pie
    st.altair_chart(juntos)


if __name__ == "__main__":
    print("Cargando streamlit")
    df = load_data("Airbnb_Locations.zip", "Airbnb_Locations.csv")

    # Textos y filtros
    add_title_and_description()
    filtered_df = show_airbnb_dataframe(df)

    # Gráficos de Mapa, Seaborn y Altair
    show_airbnb_in_map(filtered_df)
    plot_by_response_time_seaborn(filtered_df)
    interactive_view_altair(filtered_df)

    # Incluir sección ML
    pipeline = load_pipeline()
    ml_zone(pipeline)
