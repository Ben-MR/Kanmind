from django.urls import path
from .views import BoardsListViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'boards', BoardsListViewSet)
urlpatterns = router.urls

# urlpatterns = [
#     path('', BoardsListViewSet.as_view(), name='boards_list'),
# ]