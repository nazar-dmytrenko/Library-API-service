from django.urls import path
from rest_framework.routers import DefaultRouter

from borrowings.views import BorrowingViewSet

router = DefaultRouter()
router.register(r"", BorrowingViewSet, basename="borrowing")

urlpatterns = [
    path(
        "create/",
        BorrowingViewSet.as_view({"post": "create"}),
        name="book-create",
    ),
] + router.urls

app_name = "borrowings"
