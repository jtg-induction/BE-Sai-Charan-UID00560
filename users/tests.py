import json

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase

from users.serializers import CustomUserSerializer


class UserRegistrationAPIViewTestCase(APITestCase):

    def setUp(self):
        self.url = reverse("users:register")

    def test_invalid_password(self):
        """
        Test to verify that a post call with invalid passwords
        """
        user_data = {
            "first_name": "firstname",
            "last_name": "lastname",
            "email": "test@testuser.com",
            "password": "charan1234",
            "confirm_password": "INVALID_PASSWORD",
        }
        response = self.client.post(self.url, user_data)
        self.assertEqual(400, response.status_code)

    def test_user_registration(self):
        """
        Test to verify that a post call with user valid data
        """
        user_data = {
            "first_name": "firstname",
            "last_name": "lastname",
            "email": "test@testuser.com",
            "password": "charan1234",
            "confirm_password": "charan1234",
        }
        response = self.client.post(self.url, user_data)
        self.assertEqual(201, response.status_code)
        self.assertTrue("token" in json.loads(response.content))

    def test_unique_email_validation(self):
        """
        Test to verify that a post call with already exists email
        """
        user_data_1 = {
            "first_name": "firstname",
            "last_name": "lastname",
            "email": "test@testuser.com",
            "password": "charan1234",
            "confirm_password": "charan1234",
        }
        response = self.client.post(self.url, user_data_1)
        self.assertEqual(201, response.status_code)

        user_data_2 = {
            "first_name": "firstname",
            "last_name": "lastname",
            "email": "test@testuser.com",
            "password": "charan1234",
            "confirm_password": "charan1234",
        }
        response = self.client.post(self.url, user_data_2)
        self.assertEqual(400, response.status_code)


class UserLoginAPIViewTestCase(APITestCase):

    def setUp(self):
        self.url = reverse("users:login")
        self.user_data = {
            "first_name": "firstname",
            "last_name": "lastname",
            "email": "test@testuser.com",
            "password": "charan1234",
            "confirm_password": "charan1234",
        }
        serializer = CustomUserSerializer(data=self.user_data)
        if serializer.is_valid():
            serializer.save()

    def test_authentication_without_password(self):
        response = self.client.post(self.url, {"email": self.user_data["email"]})
        self.assertEqual(400, response.status_code)

    def test_authentication_with_wrong_password(self):
        response = self.client.post(
            self.url, {"email": self.user_data["email"], "password": "I_know"}
        )
        self.assertEqual(400, response.status_code)

    def test_authentication_with_valid_data(self):
        response = self.client.post(
            self.url,
            {"email": self.user_data["email"], "password": self.user_data["password"]},
        )
        self.assertEqual(200, response.status_code)
        self.assertTrue("auth_token" in json.loads(response.content))
