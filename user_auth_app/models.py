from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """
    Extension model for the built-in Django User model.

    This model stores additional profile-related information that does not
    belong directly on the User model itself.
    """

    # One-to-one relationship to the Django User.
    # Each user has exactly one profile.
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )

    # Optional short biography or description of the user.
    bio = models.TextField(
        blank=True,
        null=True,
    )

    # Optional location information (e.g. city, country).
    location = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    def __str__(self):
        """
        Return a human-readable representation of the profile.

        Uses the related user's username for display purposes
        (e.g. in Django Admin or debug output).
        """
        return self.user.username

