from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.serializers import LoginSerializer
from rest_framework import status
# Create your views here.


class LoginView(APIView):
    permission_classes=[]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(request, username=email, password=password)

            if user is not None:

                #jwt tokens
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                response_data = {
                    'access_token': access_token,
                    'refresh_token': str(refresh),
                    'user_id': user.id,
                    'name': user.full_name,
                    'email': user.email,
                    'is_customer': user.is_customer,
                    'is_superuser': user.is_superuser,
                    'is_service_provider': user.is_service_provider,
                    'is_franchisee': user.is_franchisee,
                    'is_dealer': user.is_dealer,
                }

                return Response(response_data, status=200)
            else:
                return Response({"detail": "Invalid email or password."}, status=401)
        else:
            return Response(serializer.errors, status=400)


