from django.urls import path
from . import views

urlpatterns = [
    path("books/copies/", views.CopyView.as_view()),
    path("books/copies/<int:copy_id>/", views.CopyViewDetail.as_view()),
    path("books/<int:book_id>/loans/<str:user_id>/", views.LoanView.as_view()),
    path("books/loans/", views.LoanListView.as_view()),
    path("books/devolution/<int:loan_id>/", views.LoanDetailView.as_view()),
]

