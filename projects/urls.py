from rest_framework.routers import SimpleRouter 
from django.urls import path, include
from projects.views import ProjectViewSet, ContributorViewSet
from issues_and_comments.views import IssueViewSet, CommentViewSet


project_router = SimpleRouter()
project_router.register('', ProjectViewSet, basename='project')

contributor_router = SimpleRouter()
contributor_router.register('contributors', ContributorViewSet, basename='contributor')

issue_router = SimpleRouter()
issue_router.register('issues', IssueViewSet, basename='issue')

comment_router = SimpleRouter()
comment_router.register('comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('',include(project_router.urls)),
    path('<int:project_id>/contributors/', ContributorViewSet.as_view({'get': 'list', 'post': 'create'}), name='project-contributors'),
        path('<int:project_id>/contributors/<int:pk>/', ContributorViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='project-contributor-detail'),
    path('<int:project_id>/',include(issue_router.urls)),
    path('<int:project_id>/issues/<int:issue_id>/',include(comment_router.urls)),
]
