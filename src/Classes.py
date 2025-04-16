import xml.etree.ElementTree as ET

class Partido:
    def __init__(self, fecha, jornada, local, visitante, resultado_local, resultado_visitante, goleadores=None, tarjetas=None, cambios=None):
        self.fecha = fecha  # Fecha del partido
        self.jornada = jornada  # Jornada del partido
        self.local = local  # Equipo local
        self.visitante = visitante  # Equipo visitante
        self.resultado_local = resultado_local  # Goles del equipo local
        self.resultado_visitante = resultado_visitante  # Goles del equipo visitante
        self.goleadores = goleadores if goleadores else []  # Lista de goleadores
        self.tarjetas = tarjetas if tarjetas else []  # Lista de tarjetas
        self.cambios = cambios if cambios else []  # Lista de cambios

    def to_xml(self):
        partido_elem = ET.Element("partido", fecha=self.fecha, jornada=str(self.jornada))
        ET.SubElement(partido_elem, "local").text = self.local
        ET.SubElement(partido_elem, "visitante").text = self.visitante
        ET.SubElement(partido_elem, "resultado", local=str(self.resultado_local), visitante=str(self.resultado_visitante))

        if self.goleadores:
            goleadores_elem = ET.SubElement(partido_elem, "goleadores")
            for gol in self.goleadores:
                goleadores_elem.append(gol.to_xml())

        if self.tarjetas:
            tarjetas_elem = ET.SubElement(partido_elem, "tarjetas")
            for tarjeta in self.tarjetas:
                tarjetas_elem.append(tarjeta.to_xml())

        if self.cambios:
            cambios_elem = ET.SubElement(partido_elem, "cambios")
            for cambio in self.cambios:
                cambios_elem.append(cambio.to_xml())

        return partido_elem


class Gol:
    def __init__(self, minuto, equipo, jugador):
        self.minuto = minuto  # Minuto del gol
        self.equipo = equipo  # Equipo que marcó el gol
        self.jugador = jugador  # Jugador que marcó el gol

    def to_xml(self):
        gol_elem = ET.Element("gol", minuto=self.minuto, equipo=self.equipo)
        ET.SubElement(gol_elem, "jugador").text = self.jugador
        return gol_elem


class Tarjeta:
    def __init__(self, minuto, equipo, tipo, jugador):
        self.minuto = minuto  # Minuto de la tarjeta
        self.equipo = equipo  # Equipo del jugador
        self.tipo = tipo  # Tipo de tarjeta (amarilla o roja)
        self.jugador = jugador  # Jugador que recibió la tarjeta

    def to_xml(self):
        tarjeta_elem = ET.Element("tarjeta", minuto=self.minuto, equipo=self.equipo, tipo=self.tipo)
        ET.SubElement(tarjeta_elem, "jugador").text = self.jugador
        return tarjeta_elem


class Cambio:
    def __init__(self, equipo, minuto, sale, entra):
        self.equipo = equipo  # Equipo que realizó el cambio
        self.minuto = minuto  # Minuto del cambio
        self.sale = sale  # Jugador que salió
        self.entra = entra  # Jugador que entró

    def to_xml(self):
        cambio_elem = ET.Element("cambio", equipo=self.equipo, minuto=str(self.minuto))
        ET.SubElement(cambio_elem, "sale").text = self.sale
        ET.SubElement(cambio_elem, "entra").text = self.entra
        return cambio_elem