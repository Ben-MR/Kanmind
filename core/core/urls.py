from django.contrib import admin
from django.urls import include, path
from user_auth_app.api.views import EmailCheckView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('user_auth_app.api.urls')),
    path('api/email-check/', EmailCheckView.as_view(), name='email-check'),
    path('api/', include('api.urls')),
]
