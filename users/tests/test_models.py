from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class UserModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@email.com",
            password="testpass1!",
        )

    def test_create_user(self):
        self.assertAlmostEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email, "test@email.com")
        self.assertTrue(self.user.check_password("testpass1!"))
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
            username="testadmin",
            email="admin@email.com",
            password="adminpass1!",
        )

        self.assertAlmostEqual(admin_user.username, "testadmin")
        self.assertEqual(admin_user.email, "admin@email.com")
        self.assertTrue(admin_user.check_password("adminpass1!"))
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
