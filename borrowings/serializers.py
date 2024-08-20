from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.response import Response

from books.models import Book
from borrowings.models import Borrowing

User = get_user_model()


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = "__all__"

    def create(self, request, *args, **kwargs):
        book_id = request.data.get("book_id")
        extend_return_date = request.data.get("extend_return_date")
        book = get_object_or_404(Book, id=book_id)

        if book.inventory > 0:
            with transaction.atomic():
                borrowing = Borrowing.objects.create(
                    extend_return_date=extend_return_date, user=request.user, book=book
                )
                book.inventory -= 1
                book.save()
                serializer = self.get_serializer(borrowing)

                return Response(serializer.data)

        else:
            return Response({"message": "Book is out of stock"}, status=400)


class BorrowingDetailSerializer(serializers.ModelSerializer):
    user = serializers.EmailField(source="user.email", read_only=True)
    book = serializers.CharField(source="book.title", read_only=True)

    class Meta:
        model = Borrowing
        fields = "__all__"
