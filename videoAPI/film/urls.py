from django.urls import path
from django.urls import include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('', views.FilmViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
    # path('', views.FilmListGeneric.as_view(), name='film-list'),
    # path('create/', views.FilmCreateGeneric.as_view(), name='film-create'),
    # path('<int:pk>', views.FilmDetailGeneric.as_view(), name='film-detail'),  
    
    # les noms de vues composés doivent être séparés d'un tiret(-) et 'pk' est un terme conseillé pour le bon fonctionnement des urls dans le cas des SerializersHyperLink sans avoir à faire des modifications supplémentaires dans le serializer(extra_kwargs)
    # path('', views.FilmList.as_view(), name='film-list'),
    # path('<int:pk>', views.FilmDetail.as_view(), name='film-detail'),    
    
    # path('', views.FilmList.as_view(), name='film-list'),
    # path('<int:pk>', views.FilmDetail.as_view(), name='film-detail'),

    # path('', views.film_list, name="film_list"),
    # path('<int:id>', views.film_detail, name="film_detail")
]
