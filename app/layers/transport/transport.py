# capa de transporte/comunicación con otras interfaces o sistemas externos.

import requests
from ...config import config


BASE_URL = "https://rickandmortyapi.com/api/character/"

def getAllImages(page=1, query=""):
    params = {
        "page": page,
        "name": query, 
    }

   
    response = requests.get(BASE_URL, params=params)

   
    if response.status_code != 200:
        return {"results": [], "info": {"pages": 1}}

    return response.json()
    
    # si la búsqueda no arroja resultados, entonces retornamos una lista vacía de elementos.
    if 'error' in json_response:
        print("[transport.py]: la búsqueda no arrojó resultados.")
        return json_collection

    for object in json_response['results']:
        try:
            if 'image' in object:  # verificar si la clave 'image' está presente en el objeto (sin 'image' NO nos sirve, ya que no mostrará las imágenes).
                json_collection.append(object)
            else:
                print("[transport.py]: se encontró un objeto sin clave 'image', omitiendo...")

        except KeyError: 
            # puede ocurrir que no todos los objetos tenga la info. completa, en ese caso descartamos dicho objeto y seguimos con el siguiente en la próxima iteración.
            pass

    return json_collection