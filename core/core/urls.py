from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('user_auth_app.api.urls')),
    path('api/', include('boards_app.api.urls')),
]
