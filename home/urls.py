from django.urls import path
from  home.views import BlogView ,CommentViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('blog/', BlogView.as_view()),
]