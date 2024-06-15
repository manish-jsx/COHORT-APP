# backend/urls.py

from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers
from .views import UserViewSet, CustomAuthToken
from rest_framework.authtoken import views
from allauth.account.views import ConfirmEmailView

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('admin/clearcache/', include('clearcache.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', views.obtain_auth_token),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/login/', CustomAuthToken.as_view(), name='custom_auth_token'),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    re_path(r'^auth/registration/account-confirm-email/(?P<key>[-:\w]+)/$', ConfirmEmailView.as_view(), name='account_confirm_email'),
]