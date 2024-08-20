from rest_framework import serializers

from books.models import Book, BookCover


class BookSerializer(serializers.ModelSerializer):
    cover = serializers.ChoiceField(
        choices=[(cover.name, cover.value) for cover in BookCover]
    )

    class Meta:
        model = Book
        fields = "__all__"
