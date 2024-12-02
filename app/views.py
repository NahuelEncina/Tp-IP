# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from app.layers.services.services import getAllImages 
from django.shortcuts import render

def index_page(request):
    return render(request, 'index.html')

# esta función obtiene 2 listados que corresponden a las imágenes de la API y los favoritos del usuario, y los usa para dibujar el correspondiente template.
# si el opcional de favoritos no está desarrollado, devuelve un listado vacío.

def home(request): 
    favourite_list = []
    
    page = int(request.GET.get("page", 1))
    query = request.GET.get("query", "")

 
    data = getAllImages(page=page, query=query)
    images = data["images"]
    total_pages = data["total_pages"]

    
    return render(request, "home.html", {
        "images": images,
        "current_page": page,
        "total_pages": range(1, total_pages + 1), 
        "query": query, 
    })


def search(request):
    search_msg = request.POST.get('query', '')
    if search_msg != '':
        return redirect(f"/home?query={search_msg}&page=1")
    else:
        return redirect('home')


# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    favourite_list = services.getAllFavourites(request)
    return render(request, 'favourites.html', { 'favourite_list': favourite_list })

@login_required
def saveFavourite(request):
    if request.method == 'POST':
        services.saveFavourite(request)
    return redirect('home')

@login_required
def deleteFavourite(request):
    if request.method == 'POST':
        fav_id = request.POST.get('id')
        services.deleteFavourite(request)
    return redirect('favoritos')

@login_required
def exit(request):
      logout(request)  # Cierra la sesión del usuario
      return redirect('index-page')  # Redirige a la página de inicio