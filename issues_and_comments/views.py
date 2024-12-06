from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from issues_and_comments.permissons import IsIssueAuthorOrContributor, IsCommentAuthorOrReadOnly
from issues_and_comments.models import Issue, Comment
from issues_and_comments.serializers import IssueSerializer, CommentSerializer
from projects.models import Project
from django.db.models import Q


class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsIssueAuthorOrContributor]

    def get_queryset(self):
        """
        Retourne toutes les issues du projet pour les contributeurs et l'auteur.
        """
        project_id = self.kwargs.get('project_id')
        user = self.request.user

        return Issue.objects.filter(
            Q(project_id=project_id) & (
                Q(project__contributors__user=user) |
                Q(project__author=user)
            )
        ).distinct()

    def perform_create(self, serializer):
        """
        Associe automatiquement le projet et l'auteur lors de la création.
        """
        project_id = self.kwargs.get('project_id')
        project = Project.objects.get(pk=project_id)
        serializer.save(project=project, author_user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsCommentAuthorOrReadOnly]

    def get_queryset(self):
        """
        Retourne tous les commentaires liés à une issue spécifique visible pour l'utilisateur.
        """
        user = self.request.user
        issue_id = self.kwargs.get('issue_id')  # Contexte de l'issue

        return Comment.objects.filter(
            Q(issue_id=issue_id) & (
                Q(issue__project__contributors__user=user) |
                Q(issue__project__author=user)
            )
        ).distinct()

    def perform_create(self, serializer):
        """
        Associe automatiquement l'auteur et l'issue au commentaire.
        """
        issue_id = self.kwargs.get('issue_id')
        serializer.save(issue_id=issue_id, author_user=self.request.user)