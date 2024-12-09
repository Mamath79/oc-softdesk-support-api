from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.exceptions import ValidationError
from users.models import User
from users.serializers import UserSerializer
from users.permissions import IsSelfOrAdmin


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':  # Restreindre la création d'utilisateurs
            return [IsAdminUser()]  # Seuls les administrateurs peuvent utiliser POST sur /api/users/
        if self.action in ['destroy', 'update', 'partial_update']:
            return [IsSelfOrAdmin()]  # Restriction pour les actions sensibles
        return [IsAuthenticated()]  # Par défaut, authentification requise pour les autres actions

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        partial = kwargs.pop('partial', False)

        # Vérifiez si le mot de passe est présent dans les données
        if 'password' in request.data:
            password = request.data.pop('password')
            if password:
                # Utilisez `set_password` pour chiffrer le mot de passe
                instance.set_password(password)
            else:
                raise ValidationError({"password": "Le mot de passe ne peut pas être vide."})

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class RegisterView(APIView):
    permission_classes = [AllowAny]  # Accessible à tous

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
