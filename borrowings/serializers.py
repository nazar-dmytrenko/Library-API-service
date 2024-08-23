from django.utils import timezone
from django.contrib.auth import get_user_model

from rest_framework import serializers

from borrowings.models import Borrowing
from books.models import Book

User = get_user_model()


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = "__all__"

    def validate_extend_return_date(self, value):
        if value <= timezone.now().date():
            raise serializers.ValidationError("The extend return date must be in the future.")
        return value

    def validate(self, data):
        if data["book"].inventory <= 0:
            raise serializers.ValidationError("This book is currently not available for borrowing.")
        return data

    def create(self, validated_data):
        """
            Decrease the book inventory by 1 when a borrowing is created
        """
        book = validated_data["book"]
        book.inventory -= 1
        book.save()
        return super().create(validated_data)


class BorrowingDetailSerializer(serializers.ModelSerializer):
    user = serializers.EmailField(source="user.email", read_only=True)
    book = serializers.CharField(source="book.title", read_only=True)

    class Meta:
        model = Borrowing
        fields = "__all__"
