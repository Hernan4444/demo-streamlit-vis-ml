import pyminizip
import zipfile

# Instalar pyminizip si no está instalado:
# pip install pyminizip
# o python3 -m pip install pyminizip

# Definir contraseña para el ZIP.
# Esto debería ser una variable de entorno en un entorno de producción.
# Solo por temas de demostración, se define aquí.
zip_password = "AIRBNB_DEMO_CLAVE_DEBES_SER_LARGA_Y_COMPLEJA_4444"

# Guardar el archivo CSV comprimido con contraseña.
# Asegúrate de que el archivo CSV ya existe en el directorio actual.
csv_filename = "Airbnb_Locations.csv"
zip_filename = "Airbnb_Locations.zip"

pyminizip.compress(csv_filename, None, zip_filename, zip_password, 9)


# Probar cargar el CSV desde el ZIP
with zipfile.ZipFile(zip_filename) as zf:
    try:
        print("Intentar abrir zip sin contraseña")
        # Intentar abrir el archivo CSV sin contraseña para ver si falla
        with zf.open(csv_filename) as f:
            print(f.readlines()[0].decode("UTF-8"))
    except RuntimeError:
        print("\tNo se logró")

    # Ahora abrir el archivo CSV desde el ZIP con la contraseña
    print("Intentar abrir zip con contraseña")
    with zf.open(csv_filename, pwd=zip_password.encode("UTF-8")) as f:
        print(f.readlines()[0].decode("UTF-8"))

    # Luego podemos usar pandas para leer el CSV y procesarlo en el mismo código
    # sin necesidad de descomprimirlo manualmente.
