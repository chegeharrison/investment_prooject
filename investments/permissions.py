from rest_framework import permissions

class IsAccountOwner(permissions.BasePermission):
    """
    Custom permission to check if the user is an owner of the account.
    """
    def has_object_permission(self, request, view, obj):
        return obj.account.users.filter(id=request.user.id).exists()

class CanViewAccount(permissions.BasePermission):
    """
    Permission to allow view-only access to the account.
    """
    def has_object_permission(self, request, view, obj):
        # Check if user has 'view' permission for the account
        membership = obj.accountmembership_set.filter(user=request.user, permission='view').first()
        return membership is not None

class CanManageAccount(permissions.BasePermission):
    """
    Permission to allow full CRUD access to the account.
    """
    def has_object_permission(self, request, view, obj):
        # Check if user has 'full' permission for the account
        membership = obj.accountmembership_set.filter(user=request.user, permission='full').first()
        return membership is not None

class CanPostTransaction(permissions.BasePermission):
    """
    Permission to allow posting transactions but not viewing them.
    """
    def has_object_permission(self, request, view, obj):
        # Check if user has 'post' permission for the account
        membership = obj.accountmembership_set.filter(user=request.user, permission='post').first()
        return membership is not None
