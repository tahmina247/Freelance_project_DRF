from rest_framework import permissions


class CheckClientUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'client':
            return True
        return False


class CheckOfferUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'freelancer':
            return True
        return False


class CheckEditOfferUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.freelancer