from rest_framework import viewsets, generics, permissions
from users.models import User
from users.serializers import UserSerializer, RegisterSerializer
from users.permissions import RoleBasedPermission

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [RoleBasedPermission]
    allowed_roles = ["admin", "waiter", "user"]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return User.objects.none()
        user = self.request.user
        if not user.is_authenticated:
            return User.objects.none()
        if user.role == 'admin':
            return User.objects.all()
        return User.objects.filter(id=user.id)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    permission_required = 'allow_any'