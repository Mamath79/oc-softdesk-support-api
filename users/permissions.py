from rest_framework.permissions import BasePermission


class IsSelfOrAdmin(BasePermission):
    """
    Permission pour permettre à un utilisateur de modifier/supprimer son propre profil ou pour permettre aux administrateurs d'accéder à tout.
    """

    def has_permission(self, request, view):
        # Toujours autoriser les requêtes SAFE_METHODS comme GET ou HEAD
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        # Pour les autres méthodes, on vérifie dans has_object_permission
        return True

    def has_object_permission(self, request, view, obj):
        # Autorise l'utilisateur si c'est lui-même ou un administrateur
        return request.user == obj or request.user.is_superuser

