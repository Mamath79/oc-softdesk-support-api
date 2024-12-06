from rest_framework.permissions import BasePermission, SAFE_METHODS
from projects.models import Project

# class IsContributor(BasePermission):
#     """
#     Permission permettant aux contributeurs ou auteurs d'accéder.
#     Lecture seule pour les contributeurs.
#     """
#     def has_permission(self, request, view):
#         # Vérifie que l'utilisateur est authentifié
#         if not request.user.is_authenticated:
#             return False

#         # Récupère l'identifiant du projet
#         project_id = view.kwargs.get('project_id') or view.kwargs.get('pk')
#         if not project_id:
#             return False
#         try:
#             project = Project.objects.get(pk=project_id)
#         except Project.DoesNotExist:
#             return False

#         # Vérifie si l'utilisateur est contributeur ou auteur
#         is_contributor = project.contributors.filter(user=request.user).exists()
#         is_author = project.author == request.user

#         # Si l'utilisateur est contributeur, il ne peut qu'accéder en lecture
#         if is_contributor and request.method not in SAFE_METHODS:
#             return False

#         # L'auteur a accès complet
#         return is_contributor or is_author

#     def has_object_permission(self, request, view, obj):
#         is_author = obj.author == request.user
#         is_contributor = obj.contributors.filter(user=request.user).exists()

#         # Vérifie les permissions d'objet
#         if is_contributor and request.method not in SAFE_METHODS:
#             return False
#         return is_author or is_contributor
class IsContributor(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        is_author = obj.author == request.user
        is_contributor = obj.contributors.filter(user=request.user).exists()

        if is_contributor and request.method not in SAFE_METHODS:
            return False

        return is_author or is_contributor


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
