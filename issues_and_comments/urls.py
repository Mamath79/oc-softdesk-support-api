from django.urls import path, include
from rest_framework.routers import SimpleRouter
from issues_and_comments.views import IssueViewSet, CommentViewSet

issue_router = SimpleRouter()
issue_router.register('issues', IssueViewSet, basename='issues')

comment_router = SimpleRouter()
comment_router.register('comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('projects/<int:project_id>/', include(issue_router.urls)),  
    path('projects/<int:project_id>/issues/<int:issue_id>/', include(comment_router.urls)),
]
