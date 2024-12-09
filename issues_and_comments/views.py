from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from issues_and_comments.permissions import IsIssueAuthorOrContributor, CanChangeStatus, IsCommentAuthorOrReadOnly
from issues_and_comments.models import Issue, Comment
from issues_and_comments.serializers import IssueSerializer, CommentSerializer
from django.db.models import Q
from projects.models import Project


class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            # Combine les permissions pour permettre uniquement certaines actions
            return [IsIssueAuthorOrContributor(), CanChangeStatus()]
        return [IsIssueAuthorOrContributor()]

    def get_queryset(self):
        """
        Limite les issues accessibles aux projets où l'utilisateur est contributeur ou auteur.
        """
        project_id = self.kwargs.get('project_id')
        user = self.request.user

        return Issue.objects.filter(
            Q(project_id=project_id) &
            (
                Q(project__contributors__user=user) |
                Q(project__author=user)
            )
        ).distinct()

    def perform_create(self, serializer):
        """
        Associe automatiquement le projet et l'auteur lors de la création d'une issue.
        """
        project_id = self.kwargs.get('project_id')
        project = Project.objects.get(pk=project_id)
        serializer.save(project=project, author_user=self.request.user)

    def perform_update(self, serializer):
        """
        Permet uniquement aux auteurs ou aux contributeurs assignés de mettre à jour l'issue.
        Les contributeurs peuvent modifier uniquement le statut.
        """
        issue = self.get_object()
        if issue.assigned_contributor == self.request.user and 'status' in self.request.data:
            # Mise à jour autorisée pour le statut uniquement
            serializer.save()
        elif issue.author_user == self.request.user:
            # Mise à jour complète autorisée pour l'auteur
            serializer.save()
        else:
            raise PermissionDenied("Vous n'êtes pas autorisé à modifier cette issue.")


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
