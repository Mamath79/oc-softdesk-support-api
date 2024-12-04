from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from users.models import User
from users.serializers import UserSerializer
from rest_framework.permissions import AllowAny
from users.permissions import IsSelfOrAdmin


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    

    def get_permissions(self):
        if self.action in ['destroy', 'update', 'partial_update']:
            return [IsSelfOrAdmin()]
        return [IsAuthenticated()]
    
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
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
