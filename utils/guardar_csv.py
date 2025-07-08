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

# Probar cargar el CSV desde el ZIP con contraseña.
with zipfile.ZipFile(zip_filename) as zf:
    with zf.open(csv_filename, pwd=zip_password.encode("UTF-8")) as f:
        dataset = f.readlines()
    print(dataset[0:1])
