from rest_framework import routers

from books.views import BookViewSet

router = routers.DefaultRouter()
router.register(r"books", BookViewSet)

urlpatterns = router.urls

app_name = "books"
