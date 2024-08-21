from django.test import TestCase
from borrowings.models import Borrowing
from books.models import Book
from django.contrib.auth import get_user_model
from borrowings.serializers import (
    BorrowingDetailSerializer,
    BorrowingSerializer,
)

User = get_user_model()


class BorrowingSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpassword"
        )
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="HARD",
            inventory=10,
            daily_fee="9.99",
        )
        self.borrowing = Borrowing.objects.create(
            extend_return_date="2023-07-20", book=self.book, user=self.user
        )

    def test_borrowing_serializer(self):
        serializer = BorrowingSerializer(self.borrowing)
        expected_data = {
            "id": self.borrowing.id,
            "extend_return_date": "2023-07-20",
            "book": self.book.id,
            "user": self.user.id,
            "borrow_date": str(self.borrowing.borrow_date),
            "actual_return_date": None,
        }
        self.assertEqual(serializer.data, expected_data)


class BorrowingDetailSerializerTest(TestCase):
    def setUp(self):
        # Create test data for BorrowingDetailSerializer
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpassword"
        )
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="HARDCOVER",
            inventory=10,
            daily_fee="9.99",
        )
        self.borrowing = Borrowing.objects.create(
            extend_return_date="2023-07-20", book=self.book, user=self.user
        )

    def test_borrowing_detail_serializer(self):
        serializer = BorrowingDetailSerializer(self.borrowing)
        expected_data = {
            "id": self.borrowing.id,
            "extend_return_date": "2023-07-20",
            "book": "Test Book",
            "user": "testuser@example.com",
            "borrow_date": str(self.borrowing.borrow_date),
            "actual_return_date": None,
        }
        self.assertEqual(serializer.data, expected_data)
