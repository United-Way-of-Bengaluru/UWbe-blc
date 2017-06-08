from rest_framework import serializers
from schools.models import *
from django.conf.urls import url, include
from rest_framework import routers, serializers, viewsets


# Serializers define the API representation.
class InstitutionSerializer(serializers.HyperlinkedModelSerializer):    
    class Meta:
        model = Institution
        fields = ('dise_code', 'name')

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

