
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from adminapp.serializer import CustomerSerializer,UserSerializer
from rest_framework import status
from accounts.models import Customer,User
#from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication 

# Create your views here.




class UserDetails(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]
    #authentication_classes = [TokenAuthentication]

    def post(self, request):
        customer_id = request.data.get('custom_id')  # Get customer_id from the request body
        if not customer_id:
            return Response({'error': 'Customer ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            customer = Customer.objects.select_related('user').get(custom_id=customer_id)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the customer details along with related user details
        serializer = CustomerSerializer(customer)
        return Response(serializer.data, status=status.HTTP_200_OK)