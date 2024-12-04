from rest_framework import serializers
from users.models import User
from datetime import date
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id',
                  'username',
                  'email',
                  'password',
                  'birth_date',
                  'can_be_contacted',
                  'can_data_be_shared',
                  ]
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},  # Permet de rendre le champ optionnel pour PUT
        }

    def validate_birth_date(self, value):
        """Valider que l'utilisateur a au moins 15 ans."""
        if value:
            today = date.today()
            age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
            if age < 15:
                raise serializers.ValidationError("L'âge doit être supérieur ou égal à 15 ans.")
        return value

    def create(self, validated_data):
        """Créer un utilisateur avec un mot de passe haché."""
        validated_data['password'] = make_password(validated_data['password'])  # Toujours hasher le mot de passe
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Mettre à jour un utilisateur avec hachage du mot de passe si nécessaire."""
        if 'password' in validated_data:
            instance.password = make_password(validated_data.pop('password'))  # Hacher le mot de passe
        # Mettez à jour les autres champs de l'instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
