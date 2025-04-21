import os
from lxml import etree

def validate_xml(directorio_xml, archivo_xsd):
    # Cargar el esquema XSD
    with open(archivo_xsd, "rb") as xsd_file:
        schema_root = etree.XML(xsd_file.read())
        schema = etree.XMLSchema(schema_root)

    # Iterar sobre todos los archivos XML en el directorio
    for archivo in os.listdir(directorio_xml):
        if archivo.endswith(".xml"):
            ruta_xml = os.path.join(directorio_xml, archivo)
            print(f"Validando: {ruta_xml}")

            # Cargar el archivo XML
            with open(ruta_xml, "rb") as xml_file:
                xml_doc = etree.XML(xml_file.read())

            # Validar el XML
            if schema.validate(xml_doc):
                print(f"{archivo} es válido.")
            else:
                print(f"{archivo} no es válido.")
                for error in schema.error_log:
                    print(f"  - {error.message}")
                    return False
    
    return True
