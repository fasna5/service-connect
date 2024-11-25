from rest_framework import serializers
from accounts.models import ServiceProvider

class ServiceProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model=ServiceProvider
        fields='__all__'