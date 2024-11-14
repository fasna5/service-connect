from rest_framework import viewsets
from . models import *
from . serializers import *

class Viewsetuser(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = Userserializers