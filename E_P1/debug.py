from bs4 import BeautifulSoup

# Leer el archivo HTML
with open("data/liga_16_17.html", "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

# Imprimir el HTML corregido
print(soup.prettify())