from rest_framework import serializers
from accounts.models import Customer,User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'address', 'landmark', 'email', 'phone_number', 'state', 'district']  

class CustomerSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)  

    class Meta:
        model = Customer
        fields = ['custom_id', 'profile_image', 'user_details']