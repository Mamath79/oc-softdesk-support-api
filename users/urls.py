from rest_framework import routers
from django.urls import path, include
from users.views import UserViewSet, RegisterView


router = routers.SimpleRouter()
router.register('', UserViewSet, basename='user')


urlpatterns = [
    path('register/',RegisterView.as_view(), name='register'),
    path('',include(router.urls)),
]
