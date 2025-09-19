from rest_framework.permissions import BasePermission

class IsAdminOrCreateOnly(BasePermission):
    """
    Allow anyone to create (POST) applications.
    Only admin/recruiter can do everything else.
    """

    def has_permission(self, request, view):
        if request.method == 'POST':  # public apply
            return True
        return request.user and request.user.is_staff  # admin/recruiter

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_staff  # admin/recruiter
