from rest_framework.urls import path
from .views import BookView, BookDetailView, BookFollowView, BookFollowDetailView
from copies.views import BookCopyView


urlpatterns = [
    path("books/", BookView.as_view()),
    path("books/<int:book_id>", BookDetailView.as_view()),
    path("books/<int:book_id>/follow", BookFollowView.as_view()),
    path("books/<int:book_id>/unfollow", BookFollowDetailView.as_view()),
    path("books/<int:book_id>/copies", BookCopyView.as_view()),
]
