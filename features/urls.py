from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FeaturesViewSet

router = DefaultRouter()
router.register(r'', FeaturesViewSet)  # Register the viewset

urlpatterns = [
    path('', include(router.urls)),
]