from django.conf import settings
from django.db import models


class Boards(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_boards",
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="member_boards", 
    )

    @property
    def member_count(self) -> int:
        return self.members.count()

