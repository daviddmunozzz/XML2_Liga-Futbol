from lxml import html

def extraer_enlaces_jornadas():

    # Ruta del archivo HTML descargado
    HTML_FILE = "data/liga_15_16.html"

    # Leer el archivo HTML localmente
    with open(HTML_FILE, "r", encoding="utf-8") as file:
        tree = html.parse(file)

    # Extraer todas las opciones dentro del <select> que contienen los enlaces de las jornadas
    enlaces_jornadas = tree.xpath("//select/option[contains(@value, 'div1jornada.php?jornada=')]/@value")

    # Mostrar los enlaces de cada jornada
    print("Enlaces de las jornadas extraídos:")
    for enlace in enlaces_jornadas:
        print(f"Enlace jornada: {enlace}")

    print("\nProceso completado.")

    return enlaces_jornadas

enlaces = extraer_enlaces_jornadas()