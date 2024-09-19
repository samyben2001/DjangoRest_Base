from rest_framework import serializers

from realisateur.serializers import RealisateurSerializer
from .models import Film
from realisateur.models import Realisateur

# region Basic Serializer 

# class FilmSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     titre = serializers.CharField(max_length=150)
#     description = serializers.CharField()
#     date_sortie = serializers.DateField()
#     realisateur_id = serializers.IntegerField(write_only=True)
#     realisateur = serializers.CharField(read_only=True)
      # methode appelée lors de lors d'une requete post (peut être override par le ModelSerializer)
#     def create(self, validated_data):
#         realisateur = Realisateur.objects.get(id=validated_data['realisateur_id'])
#         return Film.objects.create(realisateur=realisateur, **validated_data)
    
      # methode appelée lors de lors d'une requete update (peut être override par le ModelSerializer)
#     def update(self, instance, validated_data):

#         instance.titre = validated_data.get('titre', instance.titre)
#         instance.description = validated_data.get('description', instance.description)
#         instance.date_sortie = validated_data.get('date_sortie', instance.date_sortie)

#         realisateur_id = validated_data.get('realisateur_id', None)
#         if realisateur_id:
#             instance.realisateur = Realisateur.objects.get(id=realisateur_id)

#         instance.save()
#         return instance
# endregion

# ------------------------------------------------------------------------------------------------------

# region Model Serializer (les relations sont représentées en tant que OBJETS)
class FilmSerializer(serializers.ModelSerializer): 
    realisateur = RealisateurSerializer(read_only=True) # utilisé lors d'un avec la methode GET
    realisateur_id = serializers.PrimaryKeyRelatedField(queryset=Realisateur.objects.all(), source="realisateur", write_only=True)# utilisé lors d'un avec la methode POST
    
    class Meta:
        model = Film
        fields = ['id', 'titre', 'description', 'date_sortie', 'realisateur', 'realisateur_id']
# endregion

# ------------------------------------------------------------------------------------------------------

# region HyperLink Model Serializer (les relations sont représentées en tant que URLS)
class FilmSerializerHyperLink(serializers.HyperlinkedModelSerializer):
    realisateur = serializers.HyperlinkedRelatedField(read_only=True, view_name='realisateur-detail')

    class Meta:
        model = Film
        fields = ['id', 'url', 'titre', 'description', 'date_sortie', 'realisateur']
# endregion