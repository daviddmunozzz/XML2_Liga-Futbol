from scrapper import procesar_temporadas
from validation import validate_xml
from transform import transform2json
from load import PartidosLoader

if __name__ == "__main__":
    # Procesar temporadas y guardar resultados en XML
    procesar_temporadas()

    # Validar los XML generados
    directorio_xml = "../data/raw_xml"  
    archivo_xsd = "struct.xsd"
    es_valido = validate_xml(directorio_xml, archivo_xsd)

    # Convertir los XML a JSON
    if es_valido:
        directorio_json = "../data/json"    
        archivo_xslt = "transform2json.xslt"
        transform2json(directorio_xml, directorio_json, archivo_xslt)
    else:
        print("Los archivos XML no son válidos. No se realizará la transformación a JSON.")

    # Cargar los partidos
    PartidosLoader().cargar_partidos()