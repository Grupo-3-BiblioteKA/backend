from rest_framework import serializers
from .models import Copy, Loans
from books.models import Book
from books.serializers import BookSerializer
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta


class CopySerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    
    class Meta:
        model = Copy
        fields = ['id', 'status', 'book']


class LoanSerializer(serializers.ModelSerializer):
    date_expected_devolution = serializers.SerializerMethodField()

    # def create(self, request, *args, **kwargs):
    #     import ipdb
    #     book_found = get_object_or_404(Book, id=self.kwargs.get("book_id"))
    #     copy_borrow = Copy.objects.filter(status='Available', book=book_found).first()
    #     copy_borrow.status = 'Borrowed'
    #     copy_borrow.user.add(request.user)
    #     print(copy_borrow)
    #     copy_borrow.save()

    def get_date_expected_devolution(self, obj: Loans):
        date_now = obj.date_loan
        dead_line = timedelta(days=15)
        return date_now + dead_line

    def create(self, validated_data):
        
        return super().create(validated_data)
            
    class Meta:
        model = Loans
        fields = ['id', 'copy_id', 'user_id', 'date_loan', 'date_expected_devolution', 'date_devolution']
        read_only_fields = ['copy_id', 'user_id', 'date_loan', 'date_expected_devolution', 'date_devolution']
