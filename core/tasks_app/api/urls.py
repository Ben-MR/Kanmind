from django.urls import path
from .views import TasksViewset
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'', TasksViewset, basename="tasks")
urlpatterns = router.urls