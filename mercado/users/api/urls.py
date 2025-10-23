from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CustomAuthToken
from django.urls import path

router = DefaultRouter()
router.register(r"", UserViewSet, basename="user")

urlpatterns = [
    path('auth/', CustomAuthToken.as_view(), name='api_auth'),
]

urlpatterns += router.urls
