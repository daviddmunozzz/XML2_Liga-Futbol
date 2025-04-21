import os
import json
from pymongo import MongoClient

class PartidosLoader:
    def __init__(self, db_name="futbol", collection_name="partidos", carpeta_jsons="../data/json"):
        self.carpeta_jsons = carpeta_jsons
        self.client = MongoClient("mongodb://localhost:27017")
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def cargar_partidos(self):
        for archivo in os.listdir(self.carpeta_jsons):
            if archivo.endswith(".json"):
                ruta = os.path.join(self.carpeta_jsons, archivo)
                with open(ruta, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    temporada = data["liga"]["temporada"]
                    partidos = data["liga"]["partidos"]
                    for partido in partidos:
                        partido["temporada"] = temporada
                        # Verificar si el partido ya existe
                        if not self.collection.find_one({"fecha": partido["fecha"], "local": partido["local"], "visitante": partido["visitante"]}):
                            self.collection.insert_one(partido)
                            print(f"Partido insertado: {partido['local']} vs {partido['visitante']} ({partido['fecha']})")
                        else:
                            print(f"Partido ya existe: {partido['local']} vs {partido['visitante']} ({partido['fecha']})")
