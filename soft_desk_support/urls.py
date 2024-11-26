from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/users/', include('users.urls')),  # Routes pour les utilisateurs
    path('api/projects/', include('projects.urls')),  # Routes pour les projets et contributeurs
    path('api/issue/', include('issues_and_comments.urls')), # Routes pour les issues et commentaires
]
