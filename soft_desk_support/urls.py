from django.contrib import admin
from rest_framework import routers
from django.urls import path, include
from users.views import UserViewSet
from projects.views import ProjectViewSet


router = routers.SimpleRouter()
router.register('users', UserViewSet, basename='user')
router.register('projects', ProjectViewSet, basename='project')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/',include(router.urls))
]
