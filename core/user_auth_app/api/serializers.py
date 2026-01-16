from rest_framework import serializers
from user_auth_app.models import UserProfile
from django.contrib.auth.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile data.

    Used to create and update additional profile information
    associated with a Django User.
    """

    class Meta:
        model = UserProfile
        fields = ["user", "bio", "location"]


class RegistrationsSerializer(serializers.ModelSerializer):
    """
    Serializer used for user registration.

    Handles:
    - email-based registration
    - password confirmation
    - creation of a Django User instance
    """

    repeated_password = serializers.CharField(write_only=True)
    fullname = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["fullname", "email", "password", "repeated_password"]
        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }

    def save(self):
        """
        Create a new user after validating the passwords.

        Validation rules:
        - password and repeated_password must match
        - email must be unique

        Returns:
            User: The newly created user instance.
        """
        pw = self.validated_data["password"]
        repeated_pw = self.validated_data["repeated_password"]

        if pw != repeated_pw:
            raise serializers.ValidationError(
                {"error": "Passwords do not match"}
            )

        account = User(
            email=self.validated_data["email"],
            username=self.validated_data["email"],
        )
        account.first_name = self.validated_data["fullname"]
        account.set_password(pw)
        account.save()

        return account

    def validate_email(self, value):
        """
        Ensure the email address is unique.

        Args:
            value (str): Email address provided during registration.

        Raises:
            ValidationError: If a user with this email already exists.

        Returns:
            str: The validated email value.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Email already exists"
            )
        return value


class EmailCheckSerializer(serializers.Serializer):
    """
    Serializer used to check whether an email address
    is already registered.

    Returns basic user information if the email exists.
    """

    email = serializers.EmailField()
    exists = serializers.BooleanField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(read_only=True)

    def to_representation(self, data):
        """
        Return information about the user associated with the given email.

        If a user exists:
        - return id, email, and fullname

        If no user exists:
        - return exists = False
        """
        email = data["email"]
        user = User.objects.filter(email__iexact=email).first()

        if user:
            return {
                "id": user.id,
                "email": user.email,
                "fullname": user.first_name,
            }

        return {"exists": False}
