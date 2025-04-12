import requests
from lxml import html

# Función para obtener el HTML de una jornada
def obtener_html_jornada(enlace):
    url_base = "https://www.webprincipal.com/futbol/liga2015/division1/"  # Asegúrate de poner el dominio correcto
    url_jornada = url_base + enlace  # Concatenamos la URL base con el enlace de la jornada
    response = requests.get(url_jornada)
    if response.status_code == 200:
        return html.fromstring(response.content)
    else:
        print(f"Error al obtener la jornada {enlace}")
        return None

# Función para extraer los resultados de la jornada
def extraer_resultados_jornada(jornada_tree):
    # Extraer los partidos de la jornada (filas que contienen los resultados)
    partidos = jornada_tree.xpath("//div[@id='divresultados']//table[@class='tablaresultados']//tr[td[@class='eq1'] or td[@class='eq2']]")

    # Extraer los datos de los partidos
    for partido in partidos:
        # Intentar extraer datos para eq1/gol1
        equipo1 = partido.xpath(".//td[@class='eq1']/b/text()")
        goles1 = partido.xpath(".//td[@class='gol1']/text()")
        equipo2 = partido.xpath(".//td[@class='eq1'][2]/b/text()")
        goles2 = partido.xpath(".//td[@class='gol1'][2]/text()")

        # Si no se encuentran datos para eq1/gol1, intentar con eq2/gol2
        if not equipo1 or not goles1:
            equipo1 = partido.xpath(".//td[@class='eq2']/b/text()")
            goles1 = partido.xpath(".//td[@class='gol2']/text()")
            equipo2 = partido.xpath(".//td[@class='eq2'][2]/b/text()")
            goles2 = partido.xpath(".//td[@class='gol2'][2]/text()")

        # Verificar que todos los datos estén presentes
        if equipo1 and goles1 and equipo2 and goles2:
            print(f"{equipo1[0]} {goles1[0]} - {equipo2[0]} {goles2[0]}")
        else:
            print("Datos incompletos para un partido.")

def extraer_enlaces_jornadas():

    # Ruta del archivo HTML descargado
    HTML_FILE = "data/liga_16_17.html"

    # Leer el archivo HTML localmente
    with open(HTML_FILE, "r", encoding="utf-8") as file:
        tree = html.parse(file)

    # Extraer todas las opciones dentro del <select> que contienen los enlaces de las jornadas
    enlaces_jornadas = tree.xpath("//select/option[contains(@value, 'div1jornada.php?jornada=')]/@value")

    # Para cada enlace, imprimimos el nombre de la jornada (esto es solo para asegurarnos de que estamos extrayendo correctamente)
    for enlace in enlaces_jornadas:
        print(f"Enlace jornada: {enlace}")

    print("\nProceso completado.")
    return enlaces_jornadas

# Lista de enlaces de las jornadas (ejemplo)
enlaces_jornadas = extraer_enlaces_jornadas()

# Iterar sobre los enlaces de las jornadas y extraer los resultados
for enlace in enlaces_jornadas:
    jornada_tree = obtener_html_jornada(enlace)
    if jornada_tree:
        print(f"Resultados de la jornada {enlace}:")
        extraer_resultados_jornada(jornada_tree)
        print("\n")
