from rest_framework import serializers
from projects.models import Project, Contributor



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

class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['id',
                  'user',
                  'project',
                  'role',
                  'date_created',
                  'date_updated',
                  ]

    def validate(self, data):
        # Vérifie que l'utilisateur n'est pas déjà contributeur du projet
        if Contributor.objects.filter(user=data['user'], project=data['project']).exists():
            raise serializers.ValidationError("Cet utilisateur est déjà contributeur de ce projet.")
        return data