from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Task
from rest_framework_simplejwt.tokens import RefreshToken

# Create your tests here.
class TaskAPITestCase(APITestCase):

    def setUp(self):
        """Create test users and obtain authentication tokens"""
        self.user1 = User.objects.create_user(username="user1", password="password123")
        self.user2 = User.objects.create_user(username="user2", password="password123")
        self.admin_user = User.objects.create_superuser(username="admin", password="adminpass")

        # Get JWT tokens
        self.user1_token = self.get_jwt_token("user1", "password123")
        self.user2_token = self.get_jwt_token("user2", "password123")
        self.admin_token = self.get_jwt_token("admin", "adminpass")

        # Create a sample task for user1
        self.task1 = Task.objects.create(title="Test Task 1", description="Task description", completed=False, user=self.user1)

    def get_jwt_token(self, username, password):
        """Helper function to obtain JWT token"""
        response = self.client.post('/api/v1/token/', {"username": username, "password": password}, format='json')
        return response.data['access']

    def authenticate(self, token):
        """Helper function to authenticate a request"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_user_registration(self):
        """Test user registration API"""
        data = {"username": "newuser","password": "newpass123"}
        response = self.client.post('/api/v1/user/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_task(self):
        """Test creating a new task"""
        self.authenticate(self.user1_token)
        data = {"title": "New Task", "description": "Task description", "completed": False}
        response = self.client.post('/api/v1/tasks/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "New Task")

    def test_list_tasks(self):
        """Test retrieving tasks (should only return user's own tasks)"""
        self.authenticate(self.user1_token)
        response = self.client.get('/api/v1/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # User1 should only see their own task

    def test_update_task(self):
        """Test updating a task (only the owner can update)"""
        self.authenticate(self.user1_token)
        data = {"title": "Updated Task"}
        response = self.client.patch(f'/api/v1/tasks/{self.task1.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.title, "Updated Task")

    def test_update_task_forbidden(self):
        """Ensure another user cannot update someone else's task"""
        self.authenticate(self.user2_token)
        data = {"title": "Hacked Task"}
        response = self.client.patch(f'/api/v1/tasks/{self.task1.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_task(self):
        """Test deleting a task"""
        self.authenticate(self.user1_token)
        response = self.client.delete(f'/api/v1/tasks/{self.task1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_task_forbidden(self):
        """Ensure another user cannot delete someone else's task"""
        self.authenticate(self.user2_token)
        response = self.client.delete(f'/api/v1/tasks/{self.task1.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_filter_tasks(self):
        """Test filtering tasks by completed status"""
        self.authenticate(self.user1_token)
        response = self.client.get('/api/v1/tasks/?completed=false')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_admin_can_see_all_tasks(self):
        """Test that an admin can see all tasks"""
        self.authenticate(self.admin_token)
        response = self.client.get('/api/v1/admin/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)  # Admin should see all tasks


if __name__ == '__main__':
    import unittest
    unittest.main()
