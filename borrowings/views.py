from django.shortcuts import render
from books.models import Book
from borrowings.models import Borrowing
from borrowings.serializers import BorrowingSerializer, BorrowingDetailSerializer
from library_service import settings
from .utils import send_telegram_message

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


class BorrowingViewSet(viewsets.ModelViewSet):
    """
    Define the Borrowing ViewSet
    """
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        borrowing = serializer.save(user=self.request.user)
        serializer.save(user=self.request.user)
        bot_token = settings.TG_BOT_TOKEN
        chat_id = settings.TG_CHAT_ID
        message = f"Book '{borrowing.book.title}' has been borrowed by {self.request.user.username}."

        send_telegram_message(bot_token, chat_id, message)

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

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BorrowingDetailSerializer
        return BorrowingSerializer

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
