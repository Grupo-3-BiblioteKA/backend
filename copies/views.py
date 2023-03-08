from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework.exceptions import APIException
from .models import Copy, Loans
from books.models import Book
from users.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.permissions import IsCollaborator
from rest_framework.generics import ListAPIView, RetrieveDestroyAPIView, CreateAPIView, UpdateAPIView, ListCreateAPIView
from . serializers import CopySerializer, LoanSerializer
from django.shortcuts import get_object_or_404
from datetime import timedelta, datetime


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
        copy_borrow = Copy.objects.filter(status='Available', book=book_found).first()
        copy_borrow.status = 'Borrowed'
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

    lookup_url_kwarg = "user_id"
    lookup_url_kwarg = 'book_id'

    def perform_update(self, serializer):
        # loan_found = get_object_or_404(Loans, id)
        user_found = get_object_or_404(User, id=self.kwargs.get("user_id"))
        book_found = get_object_or_404(Book, id=self.kwargs.get("book_id"))
        user_copy = serializer.data['copy_id']
        copy_found = Copy.objects.filter(id=user_copy, book=book_found).first()
        today = datetime.now().date()

        # serializer = LoanSerializer(Loans, self.request.data, partial=True)
        
        if serializer.data['date_expected_devolution'] > today:
            user_found.date_unlock = today + timedelta(days=10)
            user_found.save()
        else:
            serializer.data['date_expected_devolution'] = None
            copy_found.status = 'Available'
            copy_found.save()
        return serializer.save(copy=copy_found, user=user_found)
