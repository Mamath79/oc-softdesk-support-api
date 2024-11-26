from rest_framework import serializers
from issues_and_comments.models import Issue, Comment
from users.models import User
from projects.models import Project


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = [
            'id',
            'title',
            'description',
            'project',
            'author_user',
            'assigned_contributor',
            'priority',
            'tag',
            'status',
            'date_created',
            'date_updated',
        ]
        read_only_fields = ['author_user', 'date_created', 'date_updated']

    def validate_assigned_contributor(self, value):
        """
        Vérifie que l'utilisateur assigné est un contributeur du projet.
        """
        project = self.initial_data.get('project')
        if not project:
            raise serializers.ValidationError("Le projet est requis.")
        project_instance = Project.objects.get(id=project)
        if value and value not in project_instance.contributors.all():
            raise serializers.ValidationError("L'utilisateur assigné doit être un contributeur du projet.")
        return value

    def create(self, validated_data):
        """
        Lors de la création, l'auteur de l'issue est automatiquement l'utilisateur connecté.
        """
        validated_data['author_user'] = self.context['request'].user
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'issue', 'author_user', 'date_created', 'date_updated']
        read_only_fields = ['author_user', 'date_created', 'date_updated']

    def create(self, validated_data):
        """
        L'auteur du commentaire est automatiquement l'utilisateur connecté.
        """
        validated_data['author_user'] = self.context['request'].user
        return super().create(validated_data)