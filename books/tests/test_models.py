from django.test import TestCase
from django.core.exceptions import ValidationError
from books.models import Book


class BookModelTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="HARD",
            inventory=10,
            daily_fee=9.99,
        )

    def test_book_str_method(self):
        self.assertEqual(str(self.book), "Test Book")

    def test_title_unique(self):
        duplicate_book = Book(
            title="Test Book",
            author="Another Author",
            cover="HARD",
            inventory=5,
            daily_fee=7.99,
        )
        with self.assertRaises(ValidationError):
            duplicate_book.full_clean()

    def test_inventory_min_value(self):
        invalid_book = Book(
            title="Invalid Book",
            author="Invalid Author",
            cover="SOFT",
            inventory=-5,
            daily_fee=4.99,
        )
        with self.assertRaises(ValidationError):
            invalid_book.full_clean()
