from django.test import TestCase

from books.serializers import BookSerializer

from decimal import Decimal


class BookSerializerTest(TestCase):
    def setUp(self):
        self.book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "cover": "HARD",
            "inventory": 10,
            "daily_fee": Decimal("9.99"),
        }

    def test_create_book(self):
        serializer = BookSerializer(data=self.book_data)
        serializer.is_valid(raise_exception=True)
        book = serializer.save()

        self.assertAlmostEqual(book.title, "Test Book")
        self.assertEqual(book.author, "Test Author")
        self.assertEqual(book.cover, "HARD")
        self.assertEqual(book.inventory, 10)
        self.assertEqual(book.daily_fee, Decimal("9.99"))