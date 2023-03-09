from rest_framework.views import status
from rest_framework.exceptions import APIException
from .models import Copy, Loans
from books.models import Book
from users.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.permissions import IsCollaborator
from rest_framework.generics import (
    ListAPIView,
    RetrieveDestroyAPIView,
    CreateAPIView,
    UpdateAPIView,
    ListCreateAPIView,
)
from .serializers import CopySerializer, LoanSerializer
from django.shortcuts import get_object_or_404, get_list_or_404
from datetime import datetime, timedelta
from rest_framework.views import Response


class CopyView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCollaborator]
    queryset = Copy.objects.all()
    serializer_class = CopySerializer


class CopyViewDetail(RetrieveDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCollaborator]
    queryset = Copy.objects.all()
    serializer_class = CopySerializer

    lookup_url_kwarg = "copy_id"


class LoanView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCollaborator]
    queryset = Loans.objects.all()
    serializer_class = LoanSerializer

    def perform_create(self, serializer):
        book_found = get_object_or_404(Book, id=self.kwargs.get("book_id"))
        # copy_borrow = Copy.objects.filter(status="Available", book=book_found).first()
        copy_borrow = get_list_or_404(Copy, status="Available", book=book_found)[0]
        # if not copy_borrow:

        copy_borrow.status = "Borrowed"
        copy_borrow.save()
        user_found = get_object_or_404(User, id=self.kwargs.get("user_id"))
        if user_found.date_unlock:
            if user_found.date_unlock <= datetime.now().date():
                user_found.date_unlock = None
                user_found.save()
                return serializer.save(copy=copy_borrow, user=user_found)
            else:
                exception = APIException(detail="User block", code="Blocked")
                exception.status_code = status.HTTP_401_UNAUTHORIZED
                raise exception
        return serializer.save(copy=copy_borrow, user=user_found)


class LoanListView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCollaborator]
    queryset = Loans.objects.filter(date_devolution=None)
    serializer_class = LoanSerializer


class LoanDetailView(UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCollaborator]
    queryset = Loans.objects.all()
    serializer_class = LoanSerializer

    lookup_url_kwarg = "loan_id"

    def perform_update(self, serializer):
        loan_found = get_object_or_404(
            Loans, id=self.kwargs.get("loan_id"), date_devolution=None
        )
        copy = get_object_or_404(Copy, id=loan_found.copy_id)
        user = get_object_or_404(User, id=loan_found.user_id)

        copy.status = "Available"
        copy.save()

        if loan_found.date_expected_devolution < datetime.now().date():
            user.date_unlock = datetime.now().date() + timedelta(days=7)
            user.save()

        return serializer.save(date_devolution=datetime.now().date())


class BookCopyView(ListCreateAPIView):
    lookup_url_kwarg = "book_id"
    queryset = Copy.objects.all()
    serializer_class = CopySerializer

    def perform_create(self, serializer):
        book_id = self.kwargs.get("book_id")
        book_obj = get_object_or_404(Book, id=book_id)

        return serializer.save(book=book_obj)

    def list(self, request, *args, **kwargs):
        queryset = Copy.objects.filter(book_id=self.kwargs.get("book_id"))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
