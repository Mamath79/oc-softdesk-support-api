from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id',
                 'username',
                 'email',
                 'age',
                 'can_be_contacted',
                 'can_data_be_shared',
                 ]
        extra_kargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['user_name'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            age=validated_data.get('age'),
            can_be_contacted=validated_data.get('can_be_contacted',False),
            can_data_be_shared=validated_data.get('can_data_be_shared',False),
        )
        return user