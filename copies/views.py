from django.shortcuts import render
from rest_framework.response import Response
from .models import Copy, Loans
from books.models import Book
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.permissions import IsCollaborator
from rest_framework.generics import ListAPIView, RetrieveDestroyAPIView, CreateAPIView
from . serializers import CopySerializer, LoanSerializer
from django.shortcuts import get_object_or_404


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
        user = self.request.user
        return serializer.save(copy=copy_borrow, user=user)
        # return super().perform_create(serializer)
