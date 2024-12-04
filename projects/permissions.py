from rest_framework.permissions import BasePermission,SAFE_METHODS
from projects.models import Project
 
class IsAdminAuthenticated(BasePermission):
 
    def has_permission(self, request, view):
    # Ne donnons l’accès qu’aux utilisateurs administrateurs authentifiés
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)
    
class IsProjectAuthor(BasePermission):
    """
    Permission pour vérifier que l'utilisateur est l'auteur du projet.
    """

    def has_permission(self, request, view):
        project_id = view.kwargs.get('project_id')
        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            return False
        return project.author == request.user

class IsContributor(BasePermission):
    """
    Permission permettant uniquement aux contributeurs ou auteurs d'accéder au projet,
    avec des restrictions pour les contributeurs (lecture seule).
    """
    def has_permission(self, request, view):
        # Autoriser les utilisateurs authentifiés
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Vérifier si l'utilisateur est contributeur ou auteur
        is_author = obj.author == request.user
        is_contributor = obj.contributors.filter(user=request.user).exists()

        # Si l'utilisateur est contributeur, il a uniquement un accès en lecture (GET, HEAD, OPTIONS)
        if is_contributor and request.method not in SAFE_METHODS:
            return False

        # L'auteur a accès complet
        return is_author or is_contributor