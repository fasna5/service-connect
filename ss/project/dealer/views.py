from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.models import ServiceProvider, BlockedUser, User
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
            dealer = request.user
            if not dealer.is_dealer:
                return Response({"detail": "You are not authorized to block a service provider."}, status=status.HTTP_403_FORBIDDEN)
            
            # Find the ServiceProvider (the blocked user)
            blocked_user = get_object_or_404(ServiceProvider, custom_id=blocked_user_custom_id)
            
            # Create the BlockedUser record
            blocked_user_record = BlockedUser.objects.create(
                blocking_user=dealer,  # The current logged-in dealer
                blocked_user=blocked_user.user,  # The service provider's user
                is_blocked=True  # Mark as blocked
            )
            
            return Response({"detail": "Service provider has been blocked."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
