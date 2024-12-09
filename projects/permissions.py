from rest_framework.permissions import BasePermission, SAFE_METHODS
from projects.models import Project


class IsContributor(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        is_author = obj.author == request.user
        is_contributor = obj.contributors.filter(user=request.user).exists()

        if is_contributor and request.method not in SAFE_METHODS:
            return False

        return is_author or is_contributor
    
class IsContributorAuthorOrReadOnly(BasePermission):
    """
    Permission permettant à l'auteur du projet de gérer les contributeurs
    et aux contributeurs d'avoir un accès en lecture seule.
    """

    def has_object_permission(self, request, view, obj):
        # Vérifiez que l'objet est bien une instance de Contributor
        if hasattr(obj, 'project'):
            is_project_author = obj.project.author == request.user
            is_contributor = obj.project.contributors.filter(user=request.user).exists()

            # Les contributeurs ont un accès en lecture seule
            if request.method in SAFE_METHODS:
                return is_contributor or is_project_author

            # Seul l'auteur du projet peut modifier ou supprimer les contributeurs
            return is_project_author

        return False


class IsProjectAuthor(BasePermission):
    """
    Permission permettant uniquement à l'auteur du projet d'avoir un accès complet.
    """
    def has_permission(self, request, view):
        project_id = view.kwargs.get('project_id') or view.kwargs.get('pk')
        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            return False
        return project.author == request.user
