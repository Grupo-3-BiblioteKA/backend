from django.shortcuts import render
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer
from copies.models import Copy


class BookView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def perform_create(self: dict, serializer):
        copies = self.request.data.pop("copies", 1)

        check_book = Book.objects.filter(**self.request.data).first()

        if check_book:
            for _ in range(copies):
                copie = Copy.objects.create(book_id=check_book.id)
            return check_book

        return serializer.save(copies=copies)


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    lookup_url_kwarg = "book_id"
