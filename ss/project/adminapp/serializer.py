from rest_framework import serializers
from accounts.models import Customer,User,Payment,ServiceRequest,Subcategory,Category, Service_Type, Collar

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'address', 'landmark', 'email', 'phone_number', 'state', 'district']  

class CustomerSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)  

    class Meta:
        model = Customer
        fields = ['custom_id', 'profile_image', 'user_details']


class PaymentSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['order_id', 'payment_date', 'amount_paid']

class ServiceRequestSerializer(serializers.ModelSerializer):
    service_provider_name = serializers.CharField(source='service_provider.full_name', read_only=True)
    # Custom field to extract date part (e.g. 2024-11-26)
    request_date = serializers.SerializerMethodField()
    
    # Custom field to extract time part (e.g. 15:32:18)
    request_time = serializers.SerializerMethodField()

    class Meta:
        model = ServiceRequest
        fields = ['title', 'service_provider_name', 'work_status', 'request_date', 'request_time']

    def get_request_date(self, obj):
        # This method will return the date part (YYYY-MM-DD)
        return obj.request_date.date() if obj.request_date else None
    
    def get_request_time(self, obj):
        # This method will return the time part (HH:MM:SS)
        return obj.request_date.time() if obj.request_date else None
    
class SubcategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Subcategory
        fields = '__all__'
