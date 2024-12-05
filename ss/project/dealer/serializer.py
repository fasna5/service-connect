from rest_framework import serializers
from accounts. models import *




class BlockUserSerializer(serializers.Serializer):
    blocked_user_custom_id = serializers.CharField(max_length=20)