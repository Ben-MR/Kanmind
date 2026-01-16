from django.db import models
from django.conf import settings
from boards_app.models import Boards
from django.utils import timezone


class Task(models.Model):
    """
    Model representing a task within a board.

    A task belongs to exactly one board and can optionally be assigned
    to a user and reviewed by another user. Tasks move through different
    workflow states (status) and have a defined priority.
    """

    class Status(models.TextChoices):
        """
        Available workflow states for a task.
        """
        TODO = "to-do", "to-do"
        IN_PROGRESS = "in-progress", "in-progress"
        REVIEW = "review", "review"
        DONE = "done", "done"

    class Priority(models.TextChoices):
        """
        Available priority levels for a task.
        """
        LOW = "low", "low"
        MEDIUM = "medium", "medium"
        HIGH = "high", "high"

    # Board this task is associated with.
    board = models.ForeignKey(
        Boards,
        on_delete=models.CASCADE,
        related_name="tasks",
    )

    # Optional short title of the task.
    title = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )

    # Optional short description of the task.
    description = models.CharField(
        max_length=250,
        blank=True,
        null=True,
    )

    # Current workflow status of the task.
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.TODO,
    )

    # Priority level of the task.
    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )

    # User responsible for completing the task.
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="assigned_tasks",
    )

    # Optional user responsible for reviewing the task.
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="review_tasks",
    )

    # Optional due date for the task.
    due_date = models.DateField(
        null=True,
        blank=True,
    )

    # Cached number of comments associated with this task.
    # This can be used for performance optimization if comment counts
    # are needed frequently.
    comments_count = models.IntegerField(default=0)


class Comment(models.Model):
    """
    Model representing a comment attached to a task.
    """

    # Task this comment belongs to.
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    # Date when the comment was created.
    created_at = models.DateField(auto_now_add=True)

    # User who authored the comment.
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments_boards",
    )

    # Text content of the comment.
    content = models.TextField(blank=True)
