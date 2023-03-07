from django.urls import path
from . import views

urlpatterns = [
    path("books/copies/", views.CopyView.as_view()),
    path("books/copies/<int:copy_id>", views.CopyViewDetail.as_view()),
    path("books/<int:book_id>/loan/", views.LoanView.as_view()),
]