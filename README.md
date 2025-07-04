# Demo Streamlit - Visualización y ML

El código de este directorio está pensado para poner en práctica las funcionalidades básicas de Streamlit de acuerdo a lo mostrado en clases. En particular, usaremos un _dataset_ de Airbnb.

## Estructura de archivos

### Carpeta `utils`
1. `Airbnb_Locations.csv`: _dataset_ original para desarrollar el _dashboard_.
2. `constantes.py`: archivo .py con algunas constantes a utilizar en `app.py`
3. `EntrenarPipeline.ipynb`: _notebook_ para entrenar modelo y guardarlo como un archivo.
4. `utils.py`: archivo .py con algunas funciones de utilidad a utilizar en `app.py`
5. `guardar_csv.py`: archivo que guarda el CSV en un ZIP con una contraseña para proteger los datos.


### Código principal

1. `Airbnb_Locations.zip`: zip protegido con el _dataset_ para desarrollar el _dashboard_.
2. `app.py`: archivo principal del _dashboard_.
3. `ml.py`: archivo .py con las funciones necesarias para agregar la sección de ML en la interfaz.
4. `requirements.txt`: librerías de Python necesarias para construir el dashboard.
5. `pipeline_model.pkl`: modelo entrenado para su posterior uso.
6. `README.md`: este archivo con el detalle de la demo.
7. `.gitignore`: archivo de `git` para indicar qué cosas no se deben subir a un repositorio de Github.

## Cómo ejecutar
1. Instalar librerías: `pip install -r requirements.txt`.
2. Crear variable de entorno (por ejemplo un `.env`) cuyo nombre es `CSV_PASSWORD` y el valor, **en este caso** es `AIRBNB_DEMO_CLAVE_DEBES_SER_LARGA_Y_COMPLEJA_4444`

> `CSV_PASSWORD=AIRBNB_DEMO_CLAVE_DEBES_SER_LARGA_Y_COMPLEJA_4444`

3. Ejecutar: `streamlit run app.py`


## Deploy _Streamlit_

En caso de subir a [Streamlit Share](https://share.streamlit.io/), ahí se ocupa formato TOML para los string, es decir, si la contraseña no es únicamente numérica, debe estar entre comillas

> `CSV_PASSWORD="AIRBNB_DEMO_CLAVE_DEBES_SER_LARGA_Y_COMPLEJA_4444"`

