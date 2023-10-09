from rest_framework import permissions


class IsPatient(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Patients').exists()


class IsDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Doctors').exists()
