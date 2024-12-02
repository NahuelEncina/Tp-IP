# capa de servicio/lógica de negocio

from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user
from app.layers.transport.transport import getAllImages as transport_getAllImages

def getAllImages(page=1, query=""):
    """
    Obtiene imágenes desde la API de Rick & Morty con soporte para paginación.
    """
     
    response = transport_getAllImages(page=page, query=query)   
    json_collection = response.get("results", [])
    total_pages = response.get("info", {}).get("pages", 1)
    

    images = []
    for datos in json_collection:
        card = translator.fromRequestIntoCard(datos)
        images.append(card)

    return {
        "images": images,
        "total_pages": total_pages
    }
# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    fav = '' # transformamos un request del template en una Card.
    fav.user = '' # le asignamos el usuario correspondiente.

    return repositories.saveFavourite(fav) # lo guardamos en la base.

# usados desde el template 'favourites.html'
def getAllFavourites(request):
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)

        favourite_list = [] # buscamos desde el repositories.py TODOS los favoritos del usuario (variable 'user').
        mapped_favourites = []

        for favourite in favourite_list:
            card = '' # transformamos cada favorito en una Card, y lo almacenamos en card.
            mapped_favourites.append(card)

        return mapped_favourites

def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.deleteFavourite(favId) # borramos un favorito por su ID.