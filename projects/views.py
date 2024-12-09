from rest_framework import viewsets
from .models import Project, Contributor
from .serializers import ProjectSerializer, ContributorSerializer
from projects.permissions import IsProjectAuthor, IsContributor, IsContributorAuthorOrReadOnly
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsProjectAuthor()]
        return [IsContributor()]

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(
            Q(author=user) | Q(contributors__user=user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ContributorViewSet(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [IsContributorAuthorOrReadOnly]

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        return Contributor.objects.filter(project_id=project_id).select_related('user')

    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_id')
        project = Project.objects.get(pk=project_id)

        # Vérifier si l'utilisateur est l'auteur du projet
        if self.request.user != project.author:
            raise PermissionDenied("Vous n'êtes pas autorisé à ajouter des contributeurs.")
        serializer.save(project=project)

    def perform_destroy(self, instance):
        # Vérifier si l'utilisateur est l'auteur du projet avant de supprimer
        project = instance.project
        if project.author != self.request.user:
            raise PermissionDenied("Vous n'êtes pas autorisé à supprimer ce contributeur.")
        instance.delete()