from rest_framework import permissions


class IsCreatorOrAdmin(permissions.BasePermission):
    """
    Object-level permission allowing only the creator of the patient record
    (or an admin/staff user) to access or modify it.
    """

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_staff or request.user.is_superuser:
            return True
        return obj.created_by == request.user
