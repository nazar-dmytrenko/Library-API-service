from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import serializers
from rest_framework.test import APIRequestFactory
from users.serializers import (
    UserLoginSerializer,
    UserRegistrationSerializer,
    UserSerializer,
)

User = get_user_model()


class UserSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )
        self.serializer = UserSerializer(instance=self.user)

    def test_user_serializer_fields(self):
        expected_fields = {"id", "username", "email"}
        self.assertEqual(set(self.serializer.fields.keys()), expected_fields)

    def test_user_serializer_data(self):
        expected_data = {
            "id": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
        }
        self.assertEqual(self.serializer.data, expected_data)


class UserRegistrationSerializerTest(TestCase):
    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "email": "test@email.com",
            "password": "testpass1",
        }

    def test_create_user(self):
        serializer = UserRegistrationSerializer(data=self.user_data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        self.assertAlmostEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@email.com")
        self.assertTrue(user.check_password("testpass1"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_user_registration_serializer_fields(self):
        expected_fields = ("id", "username", "email", "password")
        serializer = UserRegistrationSerializer(data=self.user_data)
        self.assertEqual(serializer.fields.keys(), set(expected_fields))


class UserLoginSerializerTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )
        self.data = {"email": "test@example.com", "password": "testpassword"}
        self.serializer = UserLoginSerializer(data=self.data)

    def test_user_login_serializer_fields(self):
        expected_fields = ("email", "password")
        self.assertEqual(self.serializer.fields.keys(), set(expected_fields))

    def test_user_login_serializer_validate_success(self):
        self.assertTrue(self.serializer.is_valid())
        authenticated_user = self.serializer.validate(self.data)
        self.assertEqual(authenticated_user, self.user)

    def test_user_login_serializer_validate_failure(self):
        self.data["password"] = "wrongpassword"
        self.assertFalse(self.serializer.is_valid())

        with self.assertRaises(serializers.ValidationError) as cm:
            self.serializer.validate(self.data)
        self.assertEqual(
            str(cm.exception),
            "[ErrorDetail(string='Incorrect Credentials', code='invalid')]",
        )
