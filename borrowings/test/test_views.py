from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.test import APIClient
from rest_framework import status

from books.models import Book
from borrowings.models import Borrowing

from django.contrib.auth import get_user_model
from django.test import TestCase

from datetime import date, timedelta
import json


User = get_user_model()


class BorrowingViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            username="testadminuser", email="admin-user@email.com", password="testpas1!"
        )
        self.user = User.objects.create_user(
            username="testuser", email="user@email.com", password="testpas1!"
        )

        self.first_book = Book.objects.create(
            title="Test Book 1",
            author="Test Author",
            cover="HARDCOVER",
            inventory=10,
            daily_fee="9.99",
        )

        self.second_book = Book.objects.create(
            title="Test Book 2",
            author="Test Author",
            cover="SOFT",
            inventory=10,
            daily_fee="9.99",
        )

        self.borrowing = Borrowing.objects.create(
            extend_return_date=date.today() + timedelta(days=2),
            user=self.user,
            book=self.first_book,
        )

    def get_auth_token(self, user):
        token = AccessToken.for_user(user)
        return f"Bearer {token}"

    def test_borrowing_create(self):
        token = self.get_auth_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=token)
        data = {
            "extend_return_date": str(date.today() + timedelta(days=2)),
            "book_id": self.first_book.id,
        }
        response = self.client.post(
            "/borrowings/", data=json.dumps(data), content_type="application/json"
        )
        self.first_book.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Borrowing.objects.get(id=response.data["id"]).user.email, "user@email.com"
        )
        self.assertEqual(self.first_book.inventory, 9)

    def test_get_active_borrowing(self):
        token = self.get_auth_token(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.get("/borrowings/?is_active=true")
        self.assertIsNotNone(response.data[0]["id"])
