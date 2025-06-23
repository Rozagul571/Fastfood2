# users/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, RegisterView

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
]