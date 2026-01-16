from django.conf import settings
from django.db import models


class Boards(models.Model):
    """
    Model representing a board.

    A board has:
    - a title
    - exactly one owner (creator)
    - zero or more members (users with access to the board)

    The owner is always a user and is deleted together with the board
    if the user is removed.
    """

    title = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Optional title of the board."
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_boards",
        help_text="User who owns and created the board."
    )

    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="member_boards",
        help_text="Users who are members of this board."
    )

    @property
    def member_count(self) -> int:
        """
        Return the number of members assigned to this board.

        Returns:
            int: Count of related users in the members relation.
        """
        return self.members.count()
