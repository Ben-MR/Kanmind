from django.urls import path
from .views import BoardsViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'', BoardsViewSet, basename="boards")
urlpatterns = router.urls

# urlpatterns = [
#     path('', BoardsListViewSet.as_view(), name='boards_list'),
# ]