from rest_framework import viewsets
from rest_framework.response import Response
from .models import Task, Notification
from .serializers import TaskSerializer, NotificationSerializer
from django_redis import get_redis_connection
from django.core.cache import cache


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def list(self, request, *args, **kwargs):
        user = request.user
        cache_key = f'user_tasks_{user.id}'
        redis_cache = get_redis_connection("default")
        cached_tasks = redis_cache.get(cache_key)

        if cached_tasks:
            return Response(cached_tasks)

        response = super().list(request, *args, **kwargs)
        redis_cache.set(cache_key, response.data, timeout=60*5)
        return response

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        cache_key = f'user_tasks_{request.user.id}'
        cache.delete(cache_key)
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        cache_key = f'user_tasks_{request.user.id}'
        cache.delete(cache_key)
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        cache_key = f'user_tasks_{request.user.id}'
        cache.delete(cache_key)
        return response


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
