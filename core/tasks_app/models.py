from django.db import models
from django.conf import settings
from boards_app.models import Boards
from django.utils import timezone

class Task(models.Model):
    class Status(models.TextChoices):
        TODO = 'to-do', 'to-do'
        IN_PROGRESS = 'in-progress', 'in-progress'
        REVIEW = 'review', 'review'
        DONE = 'done', 'done'

    class Priority (models.TextChoices):
        LOW = 'low', 'low'
        MEDIUM = 'medium', 'medium'
        HIGH = 'high', 'high'
    
    board = models.ForeignKey(Boards, on_delete=models.CASCADE,related_name='tasks')
    title = models.CharField(max_length=150, blank=True, null=True)
    description = models.CharField(max_length=250, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.TODO,
    )
    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="assigned_tasks",
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="review_tasks",
    )
    due_date = models.DateField(null=True, blank=True)
    comments_count = models.IntegerField(default=0)

class Comment(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    created_at= models.DateField(auto_now_add=True)
    author= models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments_boards",
    )
    content= models.TextField(blank=True)

