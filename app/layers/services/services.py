# capa de servicio/lógica de negocio

from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user
from app.layers.transport.transport import getAllImages as transport_getAllImages
from app.models import Favourite  # Importamos el modelo Favourite
from django.db import IntegrityError 

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
    if request.method == 'POST':
        # Crear una lista vacía que simula el objeto fav
        fav = []

        # Rellenar la lista con un diccionario que representa el favorito
        fav.append({
            'name': request.POST.get("name"),
            'url': request.POST.get("url"),
            'status': request.POST.get("status"),
            'last_location': request.POST.get("last_location"),
            'first_seen': request.POST.get("first_seen"),
            'user': request.user  # Asignamos el usuario autenticado
        })

        # Verificamos si el favorito ya existe en la base de datos
        existing_fav = Favourite.objects.filter(
            user=fav[0]['user'], 
            url=fav[0]['url']
        ).first()  # Buscamos si ya existe un favorito con el mismo usuario y url

        if existing_fav:
            return None  # Si ya existe, no hacemos nada y retornamos None

        # Crear un nuevo favorito en la base de datos
        try:
            # Intentamos crear el nuevo favorito
            favourite = Favourite.objects.create(
                name=fav[0]['name'],
                url=fav[0]['url'],
                status=fav[0]['status'],
                last_location=fav[0]['last_location'],
                first_seen=fav[0]['first_seen'],
                user=fav[0]['user']  # Asignamos el usuario que viene del formulario
            )
            return favourite  # Retornamos el objeto favorito creado si todo va bien

        except IntegrityError:
            # Si ocurre un error de integridad (por ejemplo, el favorito ya existe)
            return None  # Retornamos None en caso de error

    return None  # Si no es un POST, retornamos None
    return repositories.saveFavourite(fav) # lo guardamos en la base.

# usados desde el template 'favourites.html'
def getAllFavourites(request):
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)

        favourite_list = repositories.getAllFavourites(user) # buscamos desde el repositories.py TODOS los favoritos del usuario (variable 'user').
        mapped_favourites = []

    for favourite in favourite_list:
        card ={
        "id": favourite["id"],
        "name": favourite["name"],
        "url": favourite["url"],
        "status": favourite["status"],
        "last_location": favourite["last_location"],
        "first_seen": favourite["first_seen"],
    }
        mapped_favourites.append(card)

    return mapped_favourites

def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.deleteFavourite(favId) # borramos un favorito por su ID.