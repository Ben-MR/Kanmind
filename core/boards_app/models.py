from django.db import models

class Boards(models.Model):
    title = models.TextField(max_length=100, blank=True, null=True)
    member_count=models.IntegerField()
    ticket_count=models.IntegerField(default=0)
    tasks_to_do_count=models.IntegerField(default=0)
    owner_id = models.IntegerField()
    members = models.JSONField(default=list, blank=True)

