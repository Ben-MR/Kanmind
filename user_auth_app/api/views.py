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
    """
    List and create user profiles.

    - GET: Returns a list of all UserProfile objects.
    - POST: Creates a new UserProfile.

    Notes:
    - Access control depends on your global DRF settings or additional
      permission_classes added here.
    - If you want to restrict profiles to the current user only, override
      get_queryset() and/or perform_create().
    """

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a single user profile.

    - GET: Returns one UserProfile by primary key.
    - PUT/PATCH: Updates the profile.
    - DELETE: Removes the profile.

    Notes:
    - Access control depends on your global DRF settings or additional
      permission_classes added here.
    """

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class RegistrationsView(APIView):
    """
    User registration endpoint.

    Accepts registration data, creates a new user account, and returns
    a DRF auth token plus basic user information.

    Expected request fields (based on RegistrationsSerializer):
    - fullname
    - email
    - password
    - repeated_password
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Register a new user.

        On success:
        - Creates the user (password is hashed in the serializer)
        - Creates or fetches a DRF Token
        - Returns: token, fullname, email, user_id

        On validation error:
        - Returns serializer errors

        Returns:
            Response: 200 with token payload or validation errors.
        """
        serializer = RegistrationsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        saved_account = serializer.save()
        token, _ = Token.objects.get_or_create(user=saved_account)

        return Response(
            {
                "token": token.key,
                "fullname": saved_account.first_name,
                "email": saved_account.email,
                "user_id": saved_account.id,
            },
            status=200,
        )


class CustomLogin(ObtainAuthToken):
    """
    Login endpoint returning a DRF token.

    The DRF ObtainAuthToken serializer expects:
    - username
    - password

    This project uses email-based login on the frontend, so the view maps
    incoming 'email' to 'username' (the project stores username=email).
    """

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        """
        Authenticate a user and return a DRF Token.

        Frontend sends:
        - email
        - password

        DRF expects:
        - username
        - password

        Therefore:
        - if "email" is provided, it is mapped to "username" before validation.

        Returns:
            Response:
            - 200: token + basic user data
            - 400: validation/authentication errors
        """
        data = request.data.copy()

        # Frontend sends email -> DRF ObtainAuthToken expects username
        if "username" not in data and "email" in data:
            data["username"] = data["email"]

        serializer = self.serializer_class(data=data, context={"request": request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                "token": token.key,
                "fullname": user.first_name,
                "email": user.email,
                "user_id": user.id,
            },
            status=200,
        )


class LogoutView(APIView):
    """
    Logout endpoint.

    For DRF TokenAuthentication, "logout" typically means:
    - the client deletes/forgets the stored token

    This endpoint does not revoke/delete the token server-side, because
    the frontend is standardized and must remain compatible.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Confirm logout.

        Returns:
            Response: 200 with a confirmation message.
        """
        return Response({"message": "Logged out successfully"}, status=200)


class EmailCheckView(APIView):
    """
    Endpoint to check whether a given email address exists.

    - GET /...?email=someone@example.com
    - Returns user details (id/email/fullname) if present, otherwise exists=False.
    """

    serializer_class = EmailCheckSerializer

    def get(self, request):
        """
        Validate the email query parameter and return existence info.

        Query params:
            email (str): Email address to check.

        Returns:
            Response: Serialized existence information.
        """
        email = request.query_params.get("email", "")

        serializer = self.serializer_class(data={"email": email})
        
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.to_representation(serializer.validated_data))
        return Response(serializer.errors, status=404)
