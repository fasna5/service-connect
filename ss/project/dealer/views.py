from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.models import ServiceProvider, BlockedUser, User,Dealer
from .serializer import BlockUserSerializer
from django.shortcuts import get_object_or_404

class BlockServiceProviderView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        # Deserialize the request data
        serializer = BlockUserSerializer(data=request.data)
        if serializer.is_valid():
            blocked_user_custom_id = serializer.validated_data['blocked_user_custom_id']
            
            # Find the Dealer (the current user)
            logged_in_user = request.user
            
            # Step 2: Retrieve the associated Dealer instance for the logged-in user
            try:
                dealer = Dealer.objects.get(user=logged_in_user)
            except Dealer.DoesNotExist:
                return Response({"detail": "You are not associated with a dealer."}, status=status.HTTP_403_FORBIDDEN)
            
            try:
                blocked_user = ServiceProvider.objects.get(custom_id=blocked_user_custom_id, dealer=dealer)
            except ServiceProvider.DoesNotExist:
                return Response({"detail": "The specified service provider is not associated with your dealership."}, status=status.HTTP_404_NOT_FOUND)
            
            existing_blocked_user = BlockedUser.objects.filter(
                blocking_user=dealer.user,
                blocked_user=blocked_user.user,
                is_blocked=True
            ).exists()
            
            if existing_blocked_user:
                return Response({"detail": "This service provider is already blocked."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Create the BlockedUser record
            blocked_user_record = BlockedUser.objects.create(
                blocking_user=dealer.user,  # The current logged-in dealer
                blocked_user=blocked_user.user,  # The service provider's user
                is_blocked=True  # Mark as blocked
            )
            
            return Response({"detail": "Service provider has been blocked."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
