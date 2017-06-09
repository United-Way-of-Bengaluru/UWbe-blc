from rest_framework import serializers
from schools.models import *
from django.conf.urls import url, include
from rest_framework import routers, serializers, viewsets


# Serializers define the API representation.
# class InstitutionSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Institution
#         fields = ('dise_code', 'name')

        


class Institution_CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution_Category
        fields = '__all__'

class Institution_addressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution_address
        fields = '__all__'


class InstitutionSerializer(serializers.ModelSerializer):
    cat= Institution_CategorySerializer()
    inst_address = Institution_addressSerializer()
    class Meta:
        model = Institution
        fields = ('dise_code', 'name', 'cat', 'inst_address')

        
 
        
# ViewSets define the view behavior.
class InstitutionViewSet(viewsets.ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'institutes', InstitutionViewSet)


urlpatterns = [
     url(r'^', include(router.urls)),
]

