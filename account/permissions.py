from rest_framework.permissions import BasePermission

class IsInstructorUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_instructor)
    
class IsStudentUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_student)

