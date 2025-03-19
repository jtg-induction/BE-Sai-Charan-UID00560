import json

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from todos.models import Todo
from users.serializers import CustomUserSerializer


class TodoAPIViewSetTestCase(APITestCase):
    def setUp(self):
        # Create test users
        user_data1 = {
            "first_name": "User",
            "last_name": "One",
            "email": "user1@example.com",
            "password": "password123",
            "confirm_password": "password123",
        }

        user_data2 = {
            "first_name": "User",
            "last_name": "Two",
            "email": "user2@example.com",
            "password": "password123",
            "confirm_password": "password123",
        }

        serializer1 = CustomUserSerializer(data=user_data1)
        if serializer1.is_valid():
            self.user1 = serializer1.save()

        serializer2 = CustomUserSerializer(data=user_data2)
        if serializer2.is_valid():
            self.user2 = serializer2.save()

        # Create tokens for users
        self.token1 = Token.objects.create(user=self.user1)
        self.token2 = Token.objects.create(user=self.user2)

        # Create todos for both users
        self.todo1 = Todo.objects.create(
            user=self.user1,
            name="User 1 Todo",
            done=False,
        )
        self.todo2 = Todo.objects.create(
            user=self.user2,
            name="User 2 Todo",
            done=False,
        )

        # URLs
        self.list_url = reverse("todos:todos-list")
        self.detail_url1 = reverse("todos:todos-detail", kwargs={"pk": self.todo1.id})
        self.detail_url2 = reverse("todos:todos-detail", kwargs={"pk": self.todo2.id})

    def test_list_todos_unauthenticated(self):
        """
        Test to verify that unauthenticated users cannot access todos
        """
        response = self.client.get(self.list_url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_list_todos_authenticated(self):
        """
        Test to verify authenticated users can list their own todos
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token1.key}")
        response = self.client.get(self.list_url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        data = json.loads(response.content)
        self.assertEqual(1, len(data["results"]))
        self.assertEqual("User 1 Todo", data["results"][0]["todo"])

    def test_create_todo_authenticated(self):
        """
        Test to verify authenticated users can create todos
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token1.key}")
        todo_data = {"name": "New Todo Item"}
        response = self.client.post(self.list_url, todo_data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        data = json.loads(response.content)
        self.assertEqual("New Todo Item", data["name"])
        self.assertFalse(data["done"])
        self.assertTrue("date_created" in data)

    def test_retrieve_own_todo(self):
        """
        Test to verify users can retrieve their own todos
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token1.key}")
        response = self.client.get(self.detail_url1)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        data = json.loads(response.content)
        self.assertEqual(self.todo1.id, data["todo_id"])
        self.assertEqual("User 1 Todo", data["todo"])

    def test_cannot_retrieve_other_users_todo(self):
        """
        Test to verify users cannot retrieve other users' todos
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token1.key}")
        response = self.client.get(self.detail_url2)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_update_own_todo(self):
        """
        Test to verify users can update their own todos
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token1.key}")
        update_data = {
            "name": "Updated Todo",
            "done": True,
        }
        response = self.client.put(self.detail_url1, update_data, format="json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        data = json.loads(response.content)
        self.assertEqual("Updated Todo", data["name"])
        self.assertTrue(data["done"])

        self.todo1.refresh_from_db()
        self.assertEqual("Updated Todo", self.todo1.name)  # Using name field
        self.assertTrue(self.todo1.done)

    def test_cannot_update_other_users_todo(self):
        """
        Test to verify users cannot update other users' todos
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token1.key}")
        update_data = {
            "todo_id": self.todo2.id,
            "todo": "Trying to update other's todo",
            "done": True,
        }
        response = self.client.put(self.detail_url2, update_data, format="json")
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

        # Verify the original todo remains unchanged
        self.todo2.refresh_from_db()
        self.assertEqual("User 2 Todo", self.todo2.name)  # Using name field
        self.assertFalse(self.todo2.done)

    def test_delete_own_todo(self):
        """
        Test to verify users can delete their own todos
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token1.key}")
        response = self.client.delete(self.detail_url1)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        # Verify the todo was deleted
        self.assertFalse(Todo.objects.filter(id=self.todo1.id).exists())

    def test_cannot_delete_other_users_todo(self):
        """
        Test to verify users cannot delete other users' todos
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token1.key}")
        response = self.client.delete(self.detail_url2)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

        # Verify the todo still exists
        self.assertTrue(Todo.objects.filter(id=self.todo2.id).exists())

    def test_pagination(self):
        """
        Test to verify pagination works correctly
        """
        # Create multiple todos for user1
        for i in range(15):
            Todo.objects.create(
                user=self.user1,
                name=f"Todo {i}",
                done=False,
                date_created=timezone.now(),
            )

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token1.key}")
        response = self.client.get(self.list_url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        data = json.loads(response.content)
        self.assertTrue("count" in data)
        self.assertTrue("next" in data)
        self.assertTrue("previous" in data)
        self.assertTrue("results" in data)

        # Default page size should be 10
        self.assertEqual(10, len(data["results"]))
        self.assertEqual(16, data["count"])  # 15 new todos + 1 from setUp
