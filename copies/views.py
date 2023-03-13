from rest_framework.exceptions import APIException
from .models import Copy, Loan
from books.models import Book, Follow
from users.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.permissions import IsCollaborator, IsCollaboratorOrAnyone
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
from rest_framework.views import Response, status
from django.core.mail import send_mail
from django.conf import settings


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
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def perform_create(self, serializer):
        book_found = get_object_or_404(Book, id=self.kwargs.get("book_id"))

        copy_borrow = get_list_or_404(Copy, status="Available", book=book_found)[0]
        all_copies = Copy.objects.filter(status="Available", book=book_found).all()
        followers_book = Follow.objects.filter(book=book_found).all()
        followers_list = ["gabrielacamarchiori@gmail.com"]
        for follower in followers_book:
            user = User.objects.filter(id=follower.user_id).first()
            followers_list.append(user.email)

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

        if len(all_copies) <= 3 and len(all_copies) > 0:
            send_mail(
                subject="Status de livro seguido",
                message=f' O Livro "{book_found.name}" está com uma grande saída de empréstimo, como sabemos que você é fã dele, gostaríamos de te avisar que caso tenha interesse em alugá-lo em nossa BiblioteKa corra porque só temos {len(all_copies)} cópia(s) disponível(is)',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=followers_list,
                fail_silently=False,
            )

        if len(all_copies) == 0:
            send_mail(
                subject="Status de livro seguido",
                message=f' Todas as cópias do "{book_found.name}" foram emprestadas, assim que uma cópia ficar disponível enviaremos um e-mail para te avisar!',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=followers_list,
                fail_silently=False,
            )

        return serializer.save(copy=copy_borrow, user=user_found)


class LoanListView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCollaborator]
    queryset = Loan.objects.filter(date_devolution=None)
    serializer_class = LoanSerializer


class LoanDetailView(UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCollaborator]
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    lookup_url_kwarg = "loan_id"

    def perform_update(self, serializer):
        loan_found = get_object_or_404(
            Loan, id=self.kwargs.get("loan_id"), date_devolution=None
        )
        copy = get_object_or_404(Copy, id=loan_found.copy_id)
        user = get_object_or_404(User, id=loan_found.user_id)
        copy_found = Copy.objects.filter(id=copy.id).first()
        book_found = Book.objects.filter(id=copy_found.book_id).first()
        all_copies = Copy.objects.filter(status="Available", book=book_found.id).all()
        followers_book = Follow.objects.filter(book=book_found).all()
        followers_list = ["gabrielacamarchiori@gmail.com"]

        for follower in followers_book:
            user = User.objects.filter(id=follower.user_id).first()
            followers_list.append(user.email)

        copy.status = "Available"
        copy.save()

        if loan_found.date_expected_devolution < datetime.now().date():
            user.date_unlock = datetime.now().date() + timedelta(days=7)
            user.save()

        if len(all_copies) == 1:
            send_mail(
                subject="Status de livro seguido",
                message=f'Uma cópia do livro "{book_found.name}" foi devolvida, agora nós temos {len(all_copies)} cópia disponível',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=followers_list,
                fail_silently=False,
            )

        return serializer.save(date_devolution=datetime.now().date())


class BookCopyView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCollaboratorOrAnyone]
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
