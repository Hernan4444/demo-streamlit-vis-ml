import pandas as pd
import zipfile


# Definir contraseña para el ZIP.
# Esto debería ser una variable de entorno en un entorno de producción.
# Solo por temas de demostración, se define aquí.
zip_password = "AIRBNB_DEMO_CLAVE_DEBES_SER_LARGA_Y_COMPLEJA_4444"

df = pd.read_csv("Airbnb_Locations.csv")

zip_filename = "Airbnb_Locations.zip"
with zipfile.ZipFile(zip_filename, "w", compression=zipfile.ZIP_DEFLATED) as zf:
    zf.setpassword(zip_password.encode("UTF-8"))
    zf.write("Airbnb_Locations.csv")
