from rest_framework import routers
from django.urls import path, include
from projects.views import ProjectViewSet, ContributorViewSet


router = routers.SimpleRouter()
router.register('projects', ProjectViewSet, basename='project')
router.register('contributors', ContributorViewSet, basename='contributor')

urlpatterns = [
    path('api/',include(router.urls)),
]
