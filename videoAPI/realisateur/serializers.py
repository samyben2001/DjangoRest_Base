from rest_framework import serializers
from .models import Realisateur

# region Basic Serializer

# class RealisateurSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     nom = serializers.CharField(max_length=100)
#     prenom = serializers.CharField(max_length=100)
#     date_naissance = serializers.DateField(required=False, allow_null=True)


      # methode appelée lors de lors d'une requete post (peut être override par le ModelSerializer)
#     def create(self, validated_data):
#         return Realisateur.objects.create(**validated_data)
    
      # methode appelée lors de lors d'une requete update (peut être override par le ModelSerializer)
#     def update(self, instance, validated_data):
#         instance.nom = validated_data.get('nom', instance.nom)
#         instance.prenom = validated_data.get('prenom', instance.prenom)
#         instance.date_naissance = validated_data.get('date_naissance', instance.date_naissance)

#         instance.save()
#         return instance
# endregion

# ------------------------------------------------------------------------------------------------------

# region Model Serializer (les relations sont représentées en tant que OBJETS)
class RealisateurSerializer(serializers.ModelSerializer):
      class Meta:
            model = Realisateur
            fields = '__all__'     
# endregion

# region HyperLink Model Serializer (les relations sont représentées en tant que URLS)
class RealisateurSerializerHyperLink(serializers.HyperlinkedModelSerializer):
      nom = serializers.SerializerMethodField()
      
      class Meta:
            model = Realisateur
            fields = ['nom', 'url']
      
      def get_nom(self, obj):
            return f"{obj.prenom} {obj.nom}"
# endregion