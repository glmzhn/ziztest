from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, NotificationViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'notifications', NotificationViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
