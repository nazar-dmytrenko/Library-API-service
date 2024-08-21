from django.test import TestCase
from datetime import date, timedelta
from books.models import Book
from borrowings.models import Borrowing
from django.contrib.auth import get_user_model

User = get_user_model()


class BorrowingModelTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="HARD",
            inventory=10,
            daily_fee=9.99,
        )

        self.user = User.objects.create_user(
            username="testuser",
            email="test@email.com",
            password="testpass1!",
        )

        self.borrowing = Borrowing.objects.create(
            extend_return_date=date.today() + timedelta(days=2),
            book=self.book,
            user=self.user,
        )

    def test_string_representation(self):
        borrowing = self.borrowing
        extend_repr = (
            f"Borrowing: {borrowing.book.title} by User: {borrowing.user.email}"
        )
        self.assertEqual(str(borrowing), extend_repr)

    def test_borrow_date_auto_now_add(self):
        borrowing = self.borrowing
        self.assertEqual(borrowing.borrow_date, date.today())

    def test_actual_return_date_null_blank(self):
        borrowing = self.borrowing
        self.assertIsNone(borrowing.actual_return_date)

    def test_book_foreign_key(self):
        borrowing = self.borrowing
        self.assertEqual(borrowing.book, self.book)

    def test_user_foreign_key(self):
        borrowing = self.borrowing
        self.assertEqual(borrowing.user, self.user)
