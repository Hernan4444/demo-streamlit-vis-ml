import utils.constantes as C
import joblib
import streamlit as st
import pandas as pd
from utils.utils import text_to_number


@st.cache_data
def load_pipeline():
    # Cargar el modelo de ML con joblib
    return joblib.load("pipeline_model.pkl")


def predict(pipeline_loaded, info):
    """
    Predecir dato
    """
    # Dar las columnas como corresponde
    columns = [
        "tiempo_respuesta",
        "es_superhost",
        "tipo_propiedad",
        "capacidad",
        "puntaje_promedio_comunicación",
        "puntaje_promedio_localización",
        "servicio_tv_cable",
        "servicio_aire_acondicionado",
    ]

    # Construir DataFrame con los datos y columnas
    df_test = pd.DataFrame([info], columns=columns)

    # Clasificar obteniendo la probabilidad por clase
    predictions = pipeline_loaded.predict_proba(df_test)
    return {
        "classes": pipeline_loaded.classes_,
        "probabilities": predictions[0],
        "result": pipeline_loaded.predict(df_test)[0],
    }


def ml_zone(pipeline):
    """
    Sección para el formulario de predicción y su resultado
    Esta sección permite al usuario ingresar datos y obtener una predicción
    usando un modelo de Machine Learning previamente cargado.
    """
    column_1, column_2 = st.columns(2)
    column_1.subheader("Datos de entrada")
    column_2.subheader("Predicción")

    # Usamos un formulario para que el usuario ingrese los datos
    # Un form hace que cambiar el valor de los selectbox y sliders no reinicia streamlit
    # hasta que se presione el botón de form_submit_button
    form = column_1.form(key="ml_form")

    respuesta_box = form.selectbox("Tiempo de respuesta", C.TIEMPO_RESPUESTA)
    superhost_box = form.selectbox("Es superhost", C.SI_NO)
    propiedad_box = form.selectbox("Tipo Propiedad", C.TIPO_PROPIEDAD)
    capacidad_slider = form.slider("Capacidad", min_value=1, max_value=16, value=1, step=1)
    comunicacion_slider = form.slider("Puntaje Comunicación", min_value=0, max_value=10, value=5, step=1)
    localizacion_slider = form.slider("Puntaje Localización", min_value=0, max_value=10, value=5, step=1)

    tv_cable_box = form.selectbox("Tiene TV Cable", C.SI_NO)
    aire_box = form.selectbox("Tiene Aire Acondicionado", C.SI_NO)

    # Si se prsiona el botón de predecir, se ejecuta la predicción
    # y se muestra el resultado en la segunda columna
    # Se usa use_container_width=True para que el botón ocupe todo el ancho de la columna
    if form.form_submit_button("Predecir", use_container_width=True):
        info = [
            respuesta_box,
            text_to_number(superhost_box),
            propiedad_box,
            capacidad_slider,
            comunicacion_slider,
            localizacion_slider,
            text_to_number(tv_cable_box),
            text_to_number(aire_box),
        ]
        resultado = predict(pipeline, info)
        df = pd.DataFrame([resultado["probabilities"]], columns=resultado["classes"])

        column_2.write(f'Resultado: {resultado["result"]}')
        column_2.write(df)
