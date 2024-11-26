from django.urls import path, include
from rest_framework.routers import DefaultRouter
from issues_and_comments.views import IssueViewSet, CommentViewSet

router = DefaultRouter()
router.register('issue', IssueViewSet, basename='issue')
router.register('comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('projects/<int:project_id>/issues/', include(router.urls)),  # Préfixe pour les issues
    path('projects/<int:project_id>/issues/<int:issue_id>/', include(router.urls)),
]
