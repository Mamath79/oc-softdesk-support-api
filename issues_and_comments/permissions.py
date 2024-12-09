from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsIssueAuthorOrContributor(BasePermission):
    """
    Permission permettant aux contributeurs de lire les issues,
    et à l'auteur de les modifier/supprimer.
    """
    def has_permission(self, request, view):
        # Autoriser les utilisateurs authentifiés uniquement
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Autoriser les méthodes de lecture
        if request.method in SAFE_METHODS:
            return True

        # Autoriser l'auteur de l'issue à modifier ou supprimer
        return obj.author_user == request.user
    

class CanChangeStatus(BasePermission):
    """
    Permission permettant aux contributeurs assignés de modifier le statut des issues.
    """
    def has_permission(self, request, view):
        # Autoriser uniquement les utilisateurs authentifiés
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Vérifier que l'utilisateur est le contributeur assigné
        return obj.assigned_contributor == request.user


class IsCommentAuthorOrReadOnly(BasePermission):
    """
    Permission permettant à l'auteur du commentaire de le modifier ou de le supprimer.
    Les autres utilisateurs ont un accès en lecture seule.
    """
    def has_permission(self, request, view):
        # Autoriser uniquement les utilisateurs authentifiés
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Autoriser les méthodes de lecture
        if request.method in SAFE_METHODS:
            return True

        # Autoriser uniquement l'auteur à modifier ou supprimer le commentaire
        return obj.author_user == request.user
