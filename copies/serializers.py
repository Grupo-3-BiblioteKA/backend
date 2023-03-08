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

    def get_date_expected_devolution(self, obj: Loans):
        date_now = obj.date_loan
        dead_line = timedelta(days=18)
        date_sum = date_now + dead_line
        if date_sum.weekday() == 5:
            return date_sum + timedelta(days=2)
        elif date_sum.weekday() == 6:
            return date_sum + timedelta(days=1)
        return date_sum

    def create(self, validated_data):
        return super().create(validated_data)

    class Meta:
        model = Loans
        fields = ['id', 'copy_id', 'user_id', 'date_loan', 'date_expected_devolution', 'date_devolution']
        read_only_fields = ['copy_id', 'user_id', 'date_loan', 'date_expected_devolution', 'date_devolution']
