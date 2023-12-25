from rest_framework.permissions import BasePermission

class IsOwner(BaseException):
    def has_object_permission(self, request, view, obj):
        permission = request.user == obj.cust_host or request.user == obj.freel_host or request.user.is_superuser is True
        return permission

class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.email == obj.email and request.user.password == obj.password or request.user.is_superuser is True


class IsFreelancer(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and hasattr(request.user, 'professtion')
