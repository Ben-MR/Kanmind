from rest_framework.authtoken.models import Token as AuthToken
from rest_framework import generics
from user_auth_app.models import UserProfile
from .serializers import UserProfileSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegistrationsSerializer
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken

class UserProfileList(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class RegistrationsView(APIView):
    permission_classes = [AllowAny]

    def post (self, request):
        serializer = RegistrationsSerializer(data=request.data)

        if serializer.is_valid():
            saved_account = serializer.save()
            token, created = AuthToken.objects.get_or_create(user=saved_account)
            data = {
                'token':token.key,
                'fullname':saved_account.first_name,
                'email': saved_account.email,
                'user_id': saved_account.id
            }
        else:
            data = serializer.errors
    
        return Response(data)
    
    
class CustomLogin(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post (self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = AuthToken.objects.get_or_create(user=user)
            data = {
                'token':token.key,
                'fullname':user.first_name,
                'email': user.email,
                'user_id': user.id,           
            }
        else:
            data = serializer.errors
    
        return Response(data)
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"message": "Logged out successfully"}, status=200)
