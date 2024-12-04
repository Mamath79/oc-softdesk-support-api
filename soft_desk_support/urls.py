from django.contrib import admin
from django.urls import path, include
from soft_desk_support.views import api_home
from users.views import RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [
    path('', api_home, name='api-home'),

    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('api/', api_home, name='api-home'),
    path('admin/', admin.site.urls),

    path('api/users/', include('users.urls')),  # Routes pour les utilisateurs
    path('api/projects/', include('projects.urls')),  # Routes pour les projets et contributeurs
    path('api/projects/', include('issues_and_comments.urls')), # Routes pour les issues et commentaires
]
