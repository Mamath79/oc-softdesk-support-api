from rest_framework import serializers
from projects.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id',
                  'title',
                  'description',
                  'date_created',
                  'date_updated',
                  'author',
                  'type',
                  ]
    def create(self, validated_data):
        # Création d'un projet en utilisant les données validées
        project = Project.objects.create(
            title=validated_data['title'],
            description=validated_data.get('description', ''),
            author=self.context['request'].user,  # Récupère l'utilisateur connecté
            type=validated_data['type']
        )
        return project