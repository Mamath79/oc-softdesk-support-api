from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Project, Contributor
from .serializers import ProjectSerializer, ContributorSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]  # Authentification requise

    def get_queryset(self):
    # Restreint les projets visibles aux projets de l'utilisateur connecté
        return Project.objects.filter(author=self.request.user)

class ContributorViewSet(viewsets.ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filtre les contributeurs pour afficher seulement ceux des projets où l'utilisateur est contributeur
        return Contributor.objects.filter(project__contributors__user=self.request.user)