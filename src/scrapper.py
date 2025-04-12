import requests
from bs4 import BeautifulSoup
import Const  # Debes tener el archivo Const.py en el mismo directorio

def scrap_matriz_resultados(temporada):
    url = Const.URL_RESULTADO % temporada
    print(f"\nProcesando temporada: {temporada}")
    print(f"URL: {url}")
    
    try:
        res = requests.get(url)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        # Buscamos el div que contiene la tabla de resultados por su id
        matriu_div = soup.find("div", id="matriu")

        if not matriu_div:
            print("No se encontró el div con id='matriu'")
            return []

        # Buscamos la tabla dentro del div
        tabla = matriu_div.find("table", class_="taula_estil")

        if not tabla:
            print("No se encontró la tabla dentro del div 'matriu'")
            return []

        # Extraemos todas las filas (tr)
        filas = tabla.find_all("tr")
        if not filas or len(filas) < 2:
            print("La tabla no tiene suficientes filas.")
            return []

        # Primera fila: cabecera con los equipos (columnas)
        cabecera = [th.text.strip() for th in filas[0].find_all("th")[1:]]  # Ignorar la primera celda vacía

        resultados = []

        # Las demás filas son los datos (cada fila representa un equipo local)
        for i, fila in enumerate(filas[1:]):
            celdas = fila.find_all("td")
            equipo_local = cabecera[i]  # El equipo local es el mismo índice que la fila (ya que es cuadrada)
            for j, celda in enumerate(celdas):
                equipo_visitante = cabecera[j]
                resultado = celda.text.strip()
                if resultado and "-" in resultado:  # Solo consideramos celdas con resultados válidos
                    resultados.append({
                        "temporada": temporada,
                        "local": equipo_local,
                        "visitante": equipo_visitante,
                        "resultado": resultado
                    })

        print(f"{len(resultados)} partidos extraídos.")
        return resultados

    except requests.RequestException as e:
        print(f"Error al acceder a {url}: {e}")
        return []

if __name__ == "__main__":
    # Prueba con una sola temporada
    resultados_1970 = scrap_matriz_resultados("1970-71")

    # Muestra los primeros resultados
    for partido in resultados_1970[:10]:
        print(partido)
