from rest_framework import viewsets
from .models import Project, Contributor
from .serializers import ProjectSerializer, ContributorSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from projects.permissions import IsProjectAuthor, IsContributor
from django.db.models import Q


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsProjectAuthor()]
        return [IsContributor()]
    
    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(
            Q(author=user) | Q(contributors__user=user)
        ).distinct()

class ContributorViewSet(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsProjectAuthor()]
        return [IsContributor()]

    def get_queryset(self):
        """
        Filtrer les contributeurs par projet.
        """
        project_id = self.kwargs.get('project_id')
        return Contributor.objects.filter(project_id=project_id)

    def perform_create(self, serializer):
        """
        Vérifier que l'utilisateur est l'auteur du projet avant d'ajouter un contributeur.
        """
        project_id = self.kwargs.get('project_id')
        project = Project.objects.get(pk=project_id)

        if self.request.user != project.author:
            raise PermissionDenied("Vous n'êtes pas autorisé à ajouter des contributeurs à ce projet.")

        serializer.save(project=project)

    def perform_update(self, serializer):
        """
        Vérifier que l'utilisateur est l'auteur du projet avant de modifier un contributeur.
        """
        project_id = self.kwargs.get('project_id')
        project = Project.objects.get(pk=project_id)

        if self.request.user != project.author:
            raise PermissionDenied("Vous n'êtes pas autorisé à modifier les contributeurs de ce projet.")

        serializer.save()

    def perform_destroy(self, instance):
        """
        Vérifier que l'utilisateur est l'auteur du projet avant de supprimer un contributeur.
        """
        project_id = self.kwargs.get('project_id')
        project = Project.objects.get(pk=project_id)

        if self.request.user != project.author:
            raise PermissionDenied("Vous n'êtes pas autorisé à supprimer des contributeurs de ce projet.")

        instance.delete()