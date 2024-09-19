from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from .models import Film
from .serializers import FilmSerializer, FilmSerializerHyperLink

# Create your views here.
# region Basic Views
# @csrf_exempt
# def film_list(request):
#     if request.method == 'GET':
#         films = Film.objects.all()
#         serializer = FilmSerializer(films, many=True)
#         return JsonResponse(serializer.data, safe=False)
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = FilmSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
#         return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @csrf_exempt
# def film_detail(request, id):
#     try: 
#         film = Film.objects.get(pk=id)
#     except Film.DoesNotExist:
#         return JsonResponse({'error': 'Le film n\'existe pas'}, status=status.HTTP_404_NOT_FOUND)
    
#     match request.method:
#         case 'GET':
#             serializer = FilmSerializer(film)
#             return JsonResponse(serializer.data)
#         case 'PUT':
#             data = JSONParser().parse(request)
#             serializer = FilmSerializer(film, data=data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return JsonResponse(serializer.data)
#             return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         case 'DELETE':
#             film.delete()
#             return JsonResponse({'message': f'Le film {film.titre} a été supprimé'}, status=status.HTTP_204_NO_CONTENT)
# endregion

# ------------------------------------------------------------------------------------------------------

# Create your views here.
# region @api_view Decorator Views
@api_view(['GET', 'POST'])
def film_list(request):
    if request.method == 'GET':
        films = Film.objects.all()
        serializer = FilmSerializer(films, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = FilmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def film_detail(request, id):
    try: 
        film = Film.objects.get(pk=id)
    except Film.DoesNotExist:
        return Response({'error': 'Le film n\'existe pas'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = FilmSerializer(film)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = FilmSerializer(film, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        film.delete()
        return Response({'message': f'Le film {film.titre} a été supprimé'}, status=status.HTTP_204_NO_CONTENT)
# endregion

# ------------------------------------------------------------------------------------------------------

# region Class Based Views - APIView
class FilmList(APIView):
    
    def get(self, request):
        films = Film.objects.all()
        serializer = FilmSerializerHyperLink(films, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request):
        serializer = FilmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class FilmDetail(APIView):
    def get_object(self, pk):
        try:
            return Film.objects.get(pk=pk)
        except Film.DoesNotExist:
            raise NotFound(detail='error : Le film n\'existe pas')
    
    def get(self, request, pk):
        film = self.get_object(pk)
        serializer = FilmSerializer(film)
        return Response(serializer.data)
    
    def put(self, request, pk):
        film = self.get_object(pk)
        serializer = FilmSerializer(film, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        film = self.get_object(pk)
        film.delete()
        return Response({'message': 'Le film a été supprimé'}, status=status.HTTP_204_NO_CONTENT)
# endregion

# ------------------------------------------------------------------------------------------------------

# region Generic Views
class FilmListGeneric(ListCreateAPIView):
    queryset = Film.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter] # permet de filtrer et d'ordonner la reponse de la requête
    filterset_fields = ['titre'] # permet de filtrer par titre
    ordering_fields = ['nom', 'date_sortie'] # permet d'ordonner par nom ou date de sortie
    
    def get_serializer_class(self): # permet de modifier le serializer en fonction de l'action
        if self.request.method == 'GET':
            return FilmSerializerHyperLink
        else:
            return FilmSerializer
    

class FilmDetailGeneric(RetrieveUpdateDestroyAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    permission_classes = [IsAuthenticated] # le client doit être authentifié pour accéder aux methodes de la classe
# endregion

# ------------------------------------------------------------------------------------------------------

# region ViewSets
class FilmViewSet(ModelViewSet):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
# endregion
