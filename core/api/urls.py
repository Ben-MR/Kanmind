from django.urls import path, include

urlpatterns = [
    path("boards/", include("boards_app.api.urls")),
    path("tasks/", include("tasks_app.api.urls")),
]