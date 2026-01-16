from django.urls import path
from .views import UserProfileList, UserProfileDetail, RegistrationsView, CustomLogin, LogoutView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('profiles/', UserProfileList.as_view(), name='userprofile-list'),
    path('profiles/<int:pk>/', UserProfileDetail.as_view(), name='userprofile-detail'),
    path('registration/', RegistrationsView.as_view(), name='registration'),
    path('login/', CustomLogin.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

]