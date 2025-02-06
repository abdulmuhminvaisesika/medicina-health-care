from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners to add, edit, or delete products.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and is an owner
        return request.user.is_authenticated and request.user.is_owner

class IsCustomer(permissions.BasePermission):
    """
    Custom permission to only allow customers to view products.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and is a customer
        return request.user.is_authenticated and request.user.is_customer
