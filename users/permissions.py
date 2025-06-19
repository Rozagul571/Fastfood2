from rest_framework.permissions import BasePermission

class RoleBasedPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        print(user)
        if not user or not user.is_authenticated:
            return False
        if user.role == 'admin':
            return True
        allowed_roles = getattr(view, "allowed_roles", None)
        if allowed_roles and user.role in allowed_roles:
            return True
        if getattr(view, "basename", None) == "user":
            return request.method in ("GET", "HEAD", "OPTIONS")
        return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if user.role == 'admin':
            return True
        if user.role == 'waiter':
            if hasattr(obj, "waiters"):
                return user in obj.waiters.all()
            if hasattr(obj, "restaurant"):
                return user in obj.restaurant.waiters.all()
        if user.role == 'user':
            if hasattr(obj, "user"):
                return obj.user == user
        return False