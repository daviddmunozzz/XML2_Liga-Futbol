# Cambiar a src si se quiere ejecutar el script
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
from Classes import Partido, Gol, Tarjeta, Cambio

def generar_xml(partidos):
    liga_elem = ET.Element("liga")
    for partido in partidos:
        liga_elem.append(partido.to_xml())

    # Convertir a string con formato bonito
    return ET.tostring(liga_elem, encoding="unicode", method="xml")


# Ejemplo de uso
partido = Partido(
    fecha="2024-05-24",
    jornada=38,
    local="Girona",
    visitante="Granada",
    resultado_local=7,
    resultado_visitante=0,
    goleadores=[
        Gol(minuto="30", equipo="Girona", jugador="Dovbyk"),
        Gol(minuto="45+1", equipo="Girona", jugador="Portu"),
        Gol(minuto="50", equipo="Girona", jugador="Stuani"),
    ],
    tarjetas=[
        Tarjeta(minuto="12", equipo="Granada", tipo="amarilla", jugador="Neva"),
        Tarjeta(minuto="67", equipo="Girona", tipo="roja", jugador="Blind"),
        Tarjeta(minuto="80", equipo="Granada", tipo="amarilla", jugador="Uzuni"),
    ],
    cambios=[
        Cambio(equipo="Girona", minuto=60, sale="Portu", entra="Valery"),
        Cambio(equipo="Granada", minuto=70, sale="Neva", entra="Callejón"),
    ]
)

xml_resultado = generar_xml([partido])
print(xml_resultado)