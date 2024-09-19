from django.urls import path
from . import views

urlpatterns = [
    # les noms de vues composés doivent être séparés d'un tiret(-) et 'pk' est un terme conseillé pour le bon fonctionnement des urls dans le cas des SerializersHyperLink sans avoir à faire des modifications supplémentaires dans le serializer(extra_kwargs)
    path('', views.FilmList.as_view(), name='film-list'),
    path('<int:pk>', views.FilmDetail.as_view(), name='film-detail')

    # path('', views.film_list, name="film_list"),
    # path('<int:id>', views.film_detail, name="film_detail")
]
