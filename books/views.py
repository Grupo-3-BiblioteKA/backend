from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.exceptions import APIException
from .models import Book, Follow
from .serializers import BookSerializer, FollowSerializer
from copies.models import Copy
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsCollaboratorOrAnyone


class BookView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCollaboratorOrAnyone]
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCollaboratorOrAnyone]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    lookup_url_kwarg = "book_id"


class BookFollowView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "book_id"
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def perform_create(self, serializer):
        book = get_object_or_404(Book, pk=self.kwargs["book_id"])
        follow_found = Follow.objects.filter(book=book.id, user=self.request.user.id)
        if follow_found:
            exception = APIException(
                detail="User alredy follows this book", code="Blocked"
            )
            exception.status_code = 409
            raise exception
        return serializer.save(user=self.request.user, book=book)

    def get_queryset(self):
        book = get_object_or_404(Book, pk=self.kwargs["book_id"])
        return Follow.objects.filter(book=book.id)


class BookFollowDetailView(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Follow.objects.all()

    def get_object(self):
        book = get_object_or_404(Book, pk=self.kwargs["book_id"])
        user = self.request.user.id
        return get_object_or_404(Follow, user=user, book=book.id)
