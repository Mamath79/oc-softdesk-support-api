from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from issues_and_comments.models import Issue, Comment
from issues_and_comments.serializers import IssueSerializer, CommentSerializer
from projects.models import Project


class IssueViewSet(viewsets.ModelViewSet):
    """
    Gère les opérations CRUD pour les issues.
    """
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Limite les issues visibles à celles des projets auxquels l'utilisateur est contributeur.
        """
        user = self.request.user
        return Issue.objects.filter(project__contributors=user)

    def perform_create(self, serializer):
        """
        Lors de la création d'une issue, associe automatiquement le projet.
        """
        project_id = self.kwargs.get('project_id')
        project = Project.objects.get(id=project_id)
        serializer.save(project=project, author_user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Gère les opérations CRUD pour les commentaires.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Limite les commentaires visibles aux issues accessibles par l'utilisateur connecté.
        """
        user = self.request.user
        return Comment.objects.filter(issue__project__contributors=user)

    def perform_create(self, serializer):
        """
        Associe automatiquement l'auteur et l'issue au commentaire.
        """
        issue_id = self.kwargs.get('issue_id')
        serializer.save(issue_id=issue_id, author_user=self.request.user)