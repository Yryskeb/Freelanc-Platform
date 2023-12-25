from rest_framework.permissions import BasePermission
from apps.customer.models import Customer


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        permission = request.user == obj.client 
        return permission

class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        print(obj.customer)
        return request.user.email == obj.customer or request.user.is_superuser is True

class isCustomer(BasePermission):
    def has_permission(self, request, view, obj):
        if isinstance(request.user, Customer):
            return request.user.email == obj.email and request.user.password == obj.password or request.user.is_superuser is True 

class IsFreelancer(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and hasattr(request.user, 'freelancer')
