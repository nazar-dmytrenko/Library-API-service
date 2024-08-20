from django.urls import path
from rest_framework.routers import DefaultRouter

from borrowings.views import BorrowingViewSet

router = DefaultRouter()
router.register(r"", BorrowingViewSet, basename="borrowing")

urlpatterns = [] + router.urls

app_name = "borrowings"
