from django.urls import path
from django.urls import include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter() 
router.register('', views.RealisateurViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
    # path('', views.RealisateurListGeneric.as_view(), name='realisateur-list'), 
    # path('create/', views.RealisateurCreateGeneric.as_view(), name='realisateur-create'),
    # path('<int:pk>', views.RealisateurDetailGeneric.as_view(), name='realisateur-detail'),
    
    # les noms de vues composés doivent être séparés d'un tiret(-) et 'pk' est un terme conseillé pour le bon fonctionnement des urls dans le cas des SerializersHyperLink sans avoir à faire des modifications supplémentaires dans le serializer(extra_kwargs)
    
    # path('', views.RealisateurList.as_view(), name='realisateur-list'), 
    # path('<int:pk>', views.RealisateurDetail.as_view(), name='realisateur-detail'),
    
    # path('', views.realisateur_list, name="realisateur_list"),
    # path('<int:id>', views.realisateur_detail, name="realisateur_detail"),
]
