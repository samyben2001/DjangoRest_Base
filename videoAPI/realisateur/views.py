from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.parsers import JSONParser

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Realisateur
from .serializers import RealisateurSerializer, RealisateurSerializerHyperLink
from videoAPI.permissions import IsAuthenticatedNoPost

# Create your views here.
# region Basic Views
# POST > Creation - GET > liste
# @csrf_exempt
# def realisateur_list(request): 
#     if request.method == 'GET':
#         realisateurs = Realisateur.objects.all()
#         serializer = RealisateurSerializer(realisateurs, many=True)
#         return JsonResponse(serializer.data, safe=False)
    
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = RealisateurSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
#         return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# @csrf_exempt
# # PUT > mise à jour - DELETE > Supprimer - GET > le detail
# def realisateur_detail(request, id):

#     try:
#         realisateur = Realisateur.objects.get(pk=id)
#     except:
#         return JsonResponse({'error': 'Le réalisateur n\'existe pas'}, status=status.HTTP_404_NOT_FOUND)
    
#     if request.method == 'GET':
#         serializer = RealisateurSerializer(realisateur)
#         return JsonResponse(serializer.data)
    

#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = RealisateurSerializer(realisateur, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     elif request.method == 'DELETE':
#         realisateur.delete()
#         return JsonResponse({'message': 'Le réalisateur a été supprimé'}, status=status.HTTP_204_NO_CONTENT)
# endregion

# ------------------------------------------------------------------------------------------------------

# region @api_view Decorator Views
# POST > Creation - GET > liste
@api_view(['GET', 'POST'])
def realisateur_list(request): 
    if request.method == 'GET':
        realisateurs = Realisateur.objects.all()
        serializer = RealisateurSerializer(realisateurs, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = RealisateurSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'DELETE'])
def realisateur_detail(request, id):

    try:
        realisateur = Realisateur.objects.get(pk=id)
    except:
        return Response({'error': 'Le réalisateur n\'existe pas'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = RealisateurSerializer(realisateur)
        return Response(serializer.data)
    

    elif request.method == 'PUT':
        serializer = RealisateurSerializer(realisateur, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        realisateur.delete()
        return Response({'message': 'Le réalisateur a été supprimé'}, status=status.HTTP_204_NO_CONTENT)
# endregion

# ------------------------------------------------------------------------------------------------------

# region Class Based Views
class RealisateurList(APIView):
    permission_classes = [IsAdminUser | IsAuthenticatedNoPost] # admin peut acceder à toutes les methodes alors qu'un user classic authentifié n'a accès qu'au GET
    
    def get(self, request):
        realisateurs = Realisateur.objects.all()
        serializer = RealisateurSerializerHyperLink(realisateurs, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request):
        serializer = RealisateurSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RealisateurDetail(APIView):
    permission_classes = [IsAuthenticated] # le client doit être authentifié pour accéder aux methodes de la classe
    
    def get_object(self, pk):
        try:
            return Realisateur.objects.get(pk=pk)
        except Realisateur.DoesNotExist:
            raise NotFound(detail='error : Le réalisateur n\'existe pas')
    
    def get(self, request, pk):
        realisateur = self.get_object(pk)
        serializer = RealisateurSerializer(realisateur)
        return Response(serializer.data)
    
    def put(self, request, pk):
        realisateur = self.get_object(id)
        serializer = RealisateurSerializer(realisateur, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        realisateur = self.get_object(pk)
        realisateur.delete()
        return Response({'message': 'Le réalisateur a été supprimé'}, status=status.HTTP_204_NO_CONTENT)
# endregion

# ------------------------------------------------------------------------------------------------------

# region Generic Views
class RealisateurListGeneric(ListAPIView):
    queryset = Realisateur.objects.all()
    serializer_class = RealisateurSerializerHyperLink
    
class RealisateurCreateGeneric(CreateAPIView):
    queryset = Realisateur.objects.all()
    serializer_class = RealisateurSerializer

class RealisateurDetailGeneric(RetrieveUpdateDestroyAPIView):
    queryset = Realisateur.objects.all()
    serializer_class = RealisateurSerializer
    permission_classes = [IsAuthenticated] # le client doit être authentifié pour accéder aux methodes de la classe
# endregion

# ------------------------------------------------------------------------------------------------------

# region ViewSets
class RealisateurViewSet(ModelViewSet):
    queryset = Realisateur.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nom']
    
    def get_permissions(self):
        permission_classes = []
        if self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'list':
            return RealisateurSerializerHyperLink
        return RealisateurSerializer
# endregion