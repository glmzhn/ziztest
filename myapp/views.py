from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerializer
from drf_spectacular.utils import extend_schema
from zhtest.utils import delete_cache
from zhtest.settings import CACHE_TIMEOUT
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    KEY_PREFIX = 'tasks-viewset-list'
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['status', 'due_date']
    ordering_fields = ['due_date', 'status']
    search_fields = ['title', 'description']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @method_decorator(cache_page(CACHE_TIMEOUT, key_prefix=KEY_PREFIX))
    @extend_schema(operation_id='api_v1_tasks_list')
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return response

    @extend_schema(operation_id='api_v1_task_create')
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        delete_cache(self.KEY_PREFIX)
        return response

    @extend_schema(operation_id='api_v1_task_update')
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        delete_cache(self.KEY_PREFIX)
        return response

    @extend_schema(operation_id='api_v1_task_delete')
    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        delete_cache(self.KEY_PREFIX)
        return response
