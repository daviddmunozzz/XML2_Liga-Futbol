import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import Const

import xml.etree.ElementTree as ET
from xml.dom import minidom  

BASE_URL = "https://www.bdfutbol.com/es/t/"  # Base para construir URL completa del detalle

def extraer_goles_por_indice_paridad(soup, equipo_local, equipo_visitante):
    goles = []

    # Obtener todos los divs con goles (col-6 con overflow:auto)
    bloques_equipo = soup.find_all("div", class_="col-6", style="overflow: auto;")

    for idx, contenedor in enumerate(bloques_equipo):
        equipo = equipo_local if idx % 2 == 0 else equipo_visitante
        divs_gol = contenedor.find_all("div", class_="G", title="Gol")

        for div in divs_gol:
            try:
                tr = div.find_parent("tr")
                if not tr:
                    continue
                jugador_tag = tr.find("a")
                if not jugador_tag:
                    continue
                jugador = jugador_tag.text.strip()
                minuto = div.next_sibling.strip()
                if not minuto.isdigit():
                    continue
                goles.append({
                    "minuto": minuto,
                    "equipo": equipo,
                    "jugador": jugador
                })
            except Exception as e:
                print(f"⚠️ Error extrayendo gol: {e}")
                continue

    return goles



def guardar_resultados_en_xml(resultados, temporada, nombre_archivo):
    root = ET.Element("liga")
    root.set("temporada", temporada)

    for partido in resultados:
        nodo_partido = ET.SubElement(root, "partido")
        nodo_partido.set("fecha", partido.get("fecha", ""))
        nodo_partido.set("jornada", partido.get("jornada", ""))

        local_elem = ET.SubElement(nodo_partido, "local")
        local_elem.text = partido["local"]

        visitante_elem = ET.SubElement(nodo_partido, "visitante")
        visitante_elem.text = partido["visitante"]

        # Dividir resultado en goles
        goles_local, goles_visitante = partido["resultado"].split("-")

        resultado_elem = ET.SubElement(nodo_partido, "resultado")
        resultado_elem.set("local", goles_local.strip())
        resultado_elem.set("visitante", goles_visitante.strip())

        tarjetas_elem = ET.SubElement(nodo_partido, "tarjetas")
        tarjetas_elem.set("amarillas", str(partido.get("tarjetas_amarillas", 0)))
        tarjetas_elem.set("rojas", str(partido.get("tarjetas_rojas", 0)))

        # Añadir goleadores si existen
        goleadores = partido.get("goles", [])
        if goleadores:
            goleadores_elem = ET.SubElement(nodo_partido, "goleadores")
            for gol in goleadores:
                gol_elem = ET.SubElement(goleadores_elem, "gol")
                gol_elem.set("minuto", gol["minuto"])
                gol_elem.set("equipo", gol["equipo"])
                gol_elem.set("jugador", gol["jugador"])

    xml_str = ET.tostring(root, encoding="utf-8")
    parsed = minidom.parseString(xml_str)
    pretty_xml = parsed.toprettyxml(indent="  ")

    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(pretty_xml)

    print(f"📄 Archivo XML guardado como '{nombre_archivo}'")

def contar_tarjetas(url_detalle):
    """Visita el enlace del partido y cuenta amarillas y rojas (dobles o directas)"""
    try:
        res = requests.get(url_detalle)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        amarillas = soup.find_all("div", class_="TG", title="Tarjeta Amarilla")
        rojas_dobles = soup.find_all("div", class_="TG2", title="Doble Tarjeta Amarilla")
        rojas_directas = soup.find_all("div", class_="TG2", title="Expulsión")

        return len(amarillas), len(rojas_dobles) + len(rojas_directas)

    except Exception as e:
        print(f"Error al acceder a detalles del partido: {url_detalle} — {e}")
        return 0, 0

def extraer_goles(soup, equipo_nombre):
    goleadores = []
    divs_gol = soup.find_all("div", class_="G", title="Gol")

    for div in divs_gol:
        try:
            tr = div.find_parent("tr")
            if not tr:
                continue
            jugador_tag = tr.find("a")
            if not jugador_tag:
                continue
            jugador = jugador_tag.text.strip()
            minuto = div.next_sibling.strip()
            if not minuto.isdigit():
                continue
            goleadores.append({
                "minuto": minuto,
                "equipo": equipo_nombre,
                "jugador": jugador
            })
        except Exception as e:
            print(f"⚠️ Error extrayendo gol: {e}")
            continue

    return goleadores

def scrap_matriz_resultados(temporada):
    url = Const.URL_RESULTADO % temporada
    print(f"\n🔍 Procesando temporada: {temporada}")
    
    try:
        res = requests.get(url)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        matriu_div = soup.find("div", id="matriu")
        if not matriu_div:
            print("No se encontró el div con id='matriu'")
            return []

        tabla = matriu_div.find("table", class_="taula_estil")
        filas = tabla.find_all("tr")
        if not filas or len(filas) < 2:
            print("La tabla no tiene suficientes filas.")
            return []

        cabecera = [th.text.strip() for th in filas[0].find_all("th")[1:]]
        resultados = []

        for i, fila in enumerate(filas[1:]):
            celdas = fila.find_all("td")[1:]
            print(f"Fila {i} tiene {len(celdas)} celdas, cabecera tiene {len(cabecera)} columnas")
            equipo_local = cabecera[i]
            for j, celda in enumerate(celdas):
                equipo_visitante = cabecera[j]
                resultado = celda.text.strip()

                enlace_partido = celda.find("a")
                url_detalle = None
                tarjetas_amarillas = 0
                tarjetas_rojas = 0
                goles = []

                if enlace_partido and "href" in enlace_partido.attrs:
                    href = enlace_partido["href"]
                    url_detalle = urljoin(url, href)
                    tarjetas_amarillas, tarjetas_rojas = contar_tarjetas(url_detalle)

                    # Extraer goles desde la página de detalle
                    try:
                        res_detalle = requests.get(url_detalle)
                        res_detalle.raise_for_status()
                        soup_detalle = BeautifulSoup(res_detalle.text, "html.parser")

                        goles = extraer_goles_por_indice_paridad(soup_detalle, equipo_local, equipo_visitante)

                        goles = goles_local + goles_visitante
                    except Exception as e:
                        print(f"❌ Error extrayendo goles: {e}")

                if resultado and "-" in resultado:
                    resultados.append({
                        "temporada": temporada,
                        "local": equipo_local,
                        "visitante": equipo_visitante,
                        "resultado": resultado,
                        "url_partido": url_detalle,
                        "tarjetas_amarillas": tarjetas_amarillas,
                        "tarjetas_rojas": tarjetas_rojas,
                        "goles": goles,
                        "fecha": "",
                        "jornada": ""
                    })

        print(f"✅ {len(resultados)} partidos extraídos.")
        return resultados

    except requests.RequestException as e:
        print(f"❌ Error al acceder a {url}: {e}")
        return []

if __name__ == "__main__":
    # Ejemplo con una sola temporada
    datos = scrap_matriz_resultados("2011-12")

    for partido in datos:
        print(partido)

    guardar_resultados_en_xml(datos, "2011-12", "resultados_2011-12.xml")
    print("✅ Proceso completado.")
