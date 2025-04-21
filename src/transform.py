import os
import subprocess

def transform2json(directorio_xml, directorio_json, archivo_xslt):
    """Transforma todos los archivos XML en un directorio a JSON utilizando xsltproc."""

    # Crear el directorio de salida si no existe
    os.makedirs(directorio_json, exist_ok=True)

    # Iterar sobre todos los archivos XML en el directorio
    for archivo in os.listdir(directorio_xml):
        if archivo.endswith(".xml"):
            ruta_xml = os.path.join(directorio_xml, archivo)
            ruta_json = os.path.join(directorio_json, archivo.replace(".xml", ".json"))
            print(f"Transformando {ruta_xml} a {ruta_json}...")

            # Ejecutar el comando xsltproc
            comando = f"xsltproc {archivo_xslt} {ruta_xml} > {ruta_json}"
            try:
                subprocess.run(comando, shell=True, check=True)
                print(f"✅ Transformación completada: {ruta_json}")
            except subprocess.CalledProcessError as e:
                print(f"❌ Error al transformar {ruta_xml}: {e}")