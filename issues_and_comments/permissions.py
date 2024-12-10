from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsIssueAuthorOrContributor(BasePermission):
    """
    Permission permettant aux contributeurs de lire toutes les issues,
    mais à l'auteur de les modifier ou supprimer,
    et au contributeur assigné de modifier uniquement le statut.
    """

    def has_permission(self, request, view):
        # Vérifie si l'utilisateur est authentifié
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Autoriser les méthodes de lecture (GET, HEAD, OPTIONS) pour les contributeurs
        if request.method in SAFE_METHODS:
            return (
                obj.project.contributors.filter(user=request.user).exists() or
                obj.project.author == request.user
            )

        # Autoriser les méthodes de modification (PATCH) pour le contributeur assigné
        if request.method == 'PATCH' and 'status' in request.data:
            return obj.assigned_contributor == request.user

        # Pour toutes les autres actions (POST, DELETE), seul l'auteur est autorisé
        return obj.author_user == request.user

class IsCommentAuthorOrReadOnly(BasePermission):
    """
    Permission permettant à l'auteur du commentaire de le modifier/supprimer.
    Les autres utilisateurs ont un accès en lecture seule.
    """

    def has_permission(self, request, view):
        # Autoriser uniquement les utilisateurs authentifiés
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Accès complet pour l'auteur du commentaire
        if obj.author_user == request.user:
            return True
        
        # Accès en lecture seule pour les autres
        return request.method in SAFE_METHODS