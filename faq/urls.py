from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FaqViewSet

router = DefaultRouter()
router.register(r'', FaqViewSet)

urlpatterns = [
    path('', include(router.urls)),
]