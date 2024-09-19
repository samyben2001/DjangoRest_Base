from rest_framework import permissions


class IsAuthenticatedNoPost(permissions.BasePermission): # Custom permission permettant à un utilisateur autentifié de faire toutes les requetes sauf les POST

    def has_permission(self, request, view):
        # reject any POST requests
        if request.method == 'POST':
            return False

        # Otherwise, only allow authenticated requests
        return request.user and request.user.is_authenticated