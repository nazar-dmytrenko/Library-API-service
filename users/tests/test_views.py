from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

User = get_user_model()


class UserRegistrationAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.registration_url = reverse("user:create-user")

    def test_user_registration_success(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
        }
        response = self.client.post(self.registration_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, "test@example.com")

    def test_user_registration_invalid_data(self):
        data = {
            "username": "testuser",
            "email": "invalid-email",
            "password": "testpassword",
        }
        response = self.client.post(self.registration_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)


class UserLoginAPIViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )
        self.client = APIClient()
        self.login_url = reverse("user:login-user")

    def test_user_login_success(self):
        data = {"email": "test@example.com", "password": "testpassword"}
        response = self.client.post(self.login_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data["tokens"])
        self.assertIn("refresh", response.data["tokens"])

    def test_user_login_invalid_credentials(self):
        data = {"email": "test@example.com", "password": "wrongpassword"}
        response = self.client.post(self.login_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("access", response.data)
        self.assertNotIn("refresh", response.data)


class UserLogoutAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.logout_url = reverse("user:logout-user")

        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )

        self.refresh_token = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh_token.access_token}"
        )

    def test_user_logout_success(self):
        response = self.client.post(
            self.logout_url, {"refresh": str(self.refresh_token)}
        )

        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_user_logout_no_token(self):
        response = self.client.post(self.logout_url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserAPIViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )
        self.client = APIClient()
        self.user_url = reverse("user:user-info")

    def test_user_retrieve_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.user_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "test@example.com")

    def test_user_update_success(self):
        self.client.force_authenticate(user=self.user)
        data = {"email": "updated@example.com"}
        response = self.client.patch(self.user_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get().email, "updated@example.com")
