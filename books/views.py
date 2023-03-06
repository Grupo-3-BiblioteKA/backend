from django.shortcuts import render
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer


class BookView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    lookup_url_kwarg = "book_id"
