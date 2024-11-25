from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Project
from .serializers import ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]  # Authentification requise

    def get_queryset(self):
    # Restreint les projets visibles aux projets de l'utilisateur connecté
        return Project.objects.filter(author=self.request.user)
