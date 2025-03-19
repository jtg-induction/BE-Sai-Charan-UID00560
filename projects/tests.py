import json

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from projects.models import Project, ProjectMember
from users.serializers import CustomUserSerializer


class ProjectMemberApiViewSetTestCase(APITestCase):
    """Test cases for ProjectMemberApiViewSet"""

    def setUp(self):
        """Set up initial test data"""
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

        user_data3 = {
            "first_name": "User",
            "last_name": "Three",
            "email": "user3@example.com",
            "password": "password123",
            "confirm_password": "password123",
        }

        user_data4 = {
            "first_name": "User",
            "last_name": "Four",
            "email": "user4@example.com",
            "password": "password123",
            "confirm_password": "password123",
        }

        serializer1 = CustomUserSerializer(data=user_data1)
        if serializer1.is_valid():
            self.user1 = serializer1.save()

        serializer2 = CustomUserSerializer(data=user_data2)
        if serializer2.is_valid():
            self.user2 = serializer2.save()

        serializer3 = CustomUserSerializer(data=user_data3)
        if serializer3.is_valid():
            self.user3 = serializer3.save()

        serializer4 = CustomUserSerializer(data=user_data4)
        if serializer4.is_valid():
            self.user4 = serializer4.save()

        self.project1 = Project.objects.create(name="Project 1", max_members=3)
        self.project2 = Project.objects.create(name="Project 2", max_members=3)
        self.project3 = Project.objects.create(name="Project 3", max_members=3)

        # Add user1 to project1 and project2
        ProjectMember.objects.create(member=self.user1, project=self.project1)
        ProjectMember.objects.create(member=self.user1, project=self.project2)

        self.token1 = Token.objects.create(user=self.user1)
        self.token2 = Token.objects.create(user=self.user2)

        self.project_member_url_add = reverse(
            "project-member-update",
            kwargs={"pk": self.project1.id},
        )
        self.project_member_url_remove = reverse(
            "project-member-update",
            kwargs={"pk": self.project1.id},
        )

    def test_add_user_to_project_successfully(self):
        """Test that a user can be added to a project successfully."""
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token2.key}")
        response = self.client.post(
            self.project_member_url_add,
            {"user_ids": [self.user2.id]},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.user2.id, response.data["logs"])
        self.assertEqual(
            response.data["logs"][self.user2.id],
            "User added to project successfully.",
        )

        # Verify user is added
        self.assertTrue(
            ProjectMember.objects.filter(
                member=self.user2, project=self.project1
            ).exists()
        )

    def test_cannot_add_user_exceeding_project_limit(self):
        """Test that a user cannot be added if the project has reached max members."""
        ProjectMember.objects.create(member=self.user2, project=self.project1)
        ProjectMember.objects.create(member=self.user3, project=self.project1)

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token2.key}")
        response = self.client.post(
            self.project_member_url_add,
            {"user_ids": [self.user4.id]},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["logs"][self.user4.id],
            f"Project cannot have more than {self.project1.max_members} members.",
        )

    def test_cannot_add_user_already_in_two_projects(self):
        """Test that a user cannot join more than 2 projects."""
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token2.key}")
        third_project_url = reverse(
            "project-member-update",
            kwargs={"pk": self.project3.id},
        )
        response = self.client.post(
            third_project_url, {"user_ids": [self.user1.id]}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["logs"][self.user1.id],
            "Cannot add as User is a member in two projects.",
        )

    def test_cannot_add_user_already_in_project(self):
        """Test that a user cannot be added if they are already a member of the project."""
        ProjectMember.objects.create(member=self.user2, project=self.project1)

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token2.key}")
        response = self.client.post(
            self.project_member_url_add,
            {"user_ids": [self.user2.id]},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["logs"][self.user2.id],
            "User is already a Member.",
        )

    def test_remove_user_from_project_successfully(self):
        """Test that a user can be removed from a project successfully."""
        ProjectMember.objects.create(member=self.user2, project=self.project1)

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token2.key}")
        response = self.client.delete(
            self.project_member_url_remove,
            {"user_ids": [self.user2.id]},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["logs"][self.user2.id],
            "User removed successfully.",
        )

        # Verify user is removed
        self.assertFalse(
            ProjectMember.objects.filter(
                member=self.user2, project=self.project1
            ).exists()
        )

    def test_cannot_remove_user_not_in_project(self):
        """Test that a user cannot be removed if they are not a member of the project."""
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token2.key}")
        response = self.client.delete(
            self.project_member_url_remove,
            {"user_ids": [self.user3.id]},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["logs"][self.user3.id],
            "User is not a member of project.",
        )

    def test_cannot_add_users_when_not_authenticated(self):
        """Test that users cannot add members to projects without authentication."""
        response = self.client.post(
            self.project_member_url_add,
            {"user_ids": [self.user2.id]},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cannot_remove_users_when_not_authenticated(self):
        """Test that users cannot remove members from projects without authentication."""
        response = self.client.delete(
            self.project_member_url_remove,
            {"user_ids": [self.user2.id]},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
