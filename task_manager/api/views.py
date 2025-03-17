from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Task
from .serializers import TaskSerializer, UserRegistrationSerializer
from .permissions import IsOwnerOrReadOnly


class UserRegistrationView(APIView):
    """Handles user registration."""
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskListCreateView(generics.ListCreateAPIView):
    """Handles listing and creating tasks for authenticated users."""
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['completed']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at']

    def get_queryset(self):
        """Ensure users can only see their own tasks."""
        return Task.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Handles retrieving, updating, and deleting an instance of Task."""
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        """Ensure users can only access their own tasks."""
        return Task.objects.filter(user=self.request.user)

    def get_object(self):
        """Ensure correct permission handling."""
        obj = get_object_or_404(Task, pk=self.kwargs['pk'])
        if obj.user != self.request.user:
            raise PermissionDenied("You do not have permission to access this task.")
        return obj


class AdminTaskListView(generics.ListAPIView):
    """Handles listing all tasks for admin users."""
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return Task.objects.all().order_by('-created_at')