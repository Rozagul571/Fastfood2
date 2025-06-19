from django.urls import path
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, RegisterView

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
] + router.urls