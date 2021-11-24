from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers

from api.views import UserProfileViewSet, DistanceViewset

router = routers.DefaultRouter()
router.register(r'users', UserProfileViewSet)
router.register(r'distances', DistanceViewset)

urlpatterns = [
    # djoser auth urls
    url(r'^auth/', include('djoser.urls')),
    # djoser auth jwt urls
    url(r'^auth/', include('djoser.urls.jwt')),
    # DRF router
    path('', include(router.urls)),
    # Логин GUI DRF
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
