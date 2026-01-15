from rest_framework.authtoken.models import Token as AuthToken
from rest_framework import generics
from user_auth_app.models import UserProfile
from .serializers import UserProfileSerializer, EmailCheckSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegistrationsSerializer
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

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
            token, _ = Token.objects.get_or_create(user=saved_account)
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
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        data = request.data.copy()

        # Frontend sendet email -> DRF erwartet username
        if "username" not in data and "email" in data:
            data["username"] = data["email"]

        serializer = self.serializer_class(data=data, context={"request": request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,
            "fullname": user.first_name,
            "email": user.email,
            "user_id": user.id,
        }, status=200)
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response({"message": "Logged out successfully"}, status=200)
    
class EmailCheckView(APIView):
    serializer_class = EmailCheckSerializer

    def get(self, request):
        email = request.query_params.get("email", "")

        serializer = self.serializer_class(data={"email": email})
        serializer.is_valid(raise_exception=True)

        return Response(serializer.to_representation(serializer.validated_data))
    

