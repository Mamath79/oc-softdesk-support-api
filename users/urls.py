from rest_framework import routers
from django.urls import path, include
from users.views import UserViewSet



router = routers.SimpleRouter()
router.register('', UserViewSet, basename='user')


urlpatterns = [
    path('',include(router.urls))
]
