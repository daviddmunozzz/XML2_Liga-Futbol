<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:output method="text" encoding="UTF-8" indent="yes"/>

  <!-- Comienza la transformación -->
  <xsl:template match="/">
    {
      "liga": {
        "temporada": "<xsl:value-of select='/liga/@temporada'/>",
        "partidos": [
          <xsl:for-each select="/liga/partido">
            {
              "fecha": "<xsl:value-of select='@fecha'/>",
              "jornada": "<xsl:value-of select='@jornada'/>",
              "local": "<xsl:value-of select='local'/>",
              "visitante": "<xsl:value-of select='visitante'/>",
              "resultado": {
                "local": "<xsl:value-of select='resultado/@local'/>",
                "visitante": "<xsl:value-of select='resultado/@visitante'/>"
              },
              "tarjetas": {
                "amarillas": "<xsl:value-of select='tarjetas/@amarillas'/>",
                "rojas": "<xsl:value-of select='tarjetas/@rojas'/>"
              },
              "goleadores": [
                <xsl:for-each select="goleadores/gol">
                  {
                    "minuto": "<xsl:value-of select='@minuto'/>",
                    "equipo": "<xsl:value-of select='@equipo'/>",
                    "jugador": "<xsl:value-of select='@jugador'/>"
                  }<xsl:if test="position() != last()">,</xsl:if>
                </xsl:for-each>
              ]
            }<xsl:if test="position() != last()">,</xsl:if>
          </xsl:for-each>
        ]
      }
    }
  </xsl:template>
</xsl:stylesheet>