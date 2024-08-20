from django.shortcuts import render
from books.models import Book
from borrowings.models import Borrowing
from borrowings.serializers import BorrowingSerializer, BorrowingDetailSerializer

from django.db import transaction
from django.shortcuts import get_object_or_404
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class BorrowingViewSet(viewsets.ModelViewSet):
    """
    Define the Borrowing ViewSet
    """
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = (IsAuthenticated,)

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
                message = f"New borrowing created: {borrowing.book.title} by {borrowing.user.email}"
                return Response(serializer.data)

        else:
            return Response({"message": "Book is out of stock"}, status=400)

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.GET.get("user_id")
        is_active = self.request.GET.get("is_active")

        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)

        if user_id:
            queryset = queryset.filter(user_id=user_id)

        if is_active:
            if is_active.lower() == "true":
                queryset = queryset.filter(actual_return_date__isnull=True)
            if is_active.lower() == "false":
                queryset = queryset.filter(actual_return_date__isnull=False)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = BorrowingDetailSerializer(instance)
        return Response(serializer.data)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "is_active",
                type=OpenApiTypes.BOOL,
                description="Filter if books already returned or not (ex. ?is_active=True)",
            ),
            OpenApiParameter(
                "user_id",
                type=OpenApiTypes.INT,
                description="If user is admin he can filter by user id (ex. ?user_id=1)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)
