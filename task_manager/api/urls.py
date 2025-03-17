from django.urls import path
from .views import TaskListCreateView,TaskDetailView,AdminTaskListView,UserRegistrationView

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('user/register/', UserRegistrationView.as_view(), name='user-registration'),
    path('admin/tasks/', AdminTaskListView.as_view(), name='admin-task-list'),


]


