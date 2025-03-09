from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FeaturesViewSet

router = DefaultRouter()
router.register(r'', FeaturesViewSet)

urlpatterns = [
    path('', include(router.urls)),
]