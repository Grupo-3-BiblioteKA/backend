from rest_framework import serializers
from .models import Copy, Loan
from books.serializers import BookSerializer, BookSimpleSerializer
from books.models import Book


class CopySerializer(serializers.ModelSerializer):
    book = BookSimpleSerializer(read_only=True)

    copies = serializers.IntegerField(write_only=True)

    class Meta:
        model = Copy
        fields = ["id", "status", "book", "copies"]
        read_only_fields = ["id", "status", "book"]

    def create(self, validated_data):
        copies_qtd = validated_data.pop("copies")

        new_copies = [Copy(**validated_data) for _ in range(copies_qtd)]

        copies_created = Copy.objects.bulk_create(new_copies)

        return copies_created


class LoanSerializer(serializers.ModelSerializer):
    book = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Loan
        fields = [
            "id",
            "copy_id",
            "user_id",
            "date_loan",
            "date_expected_devolution",
            "date_devolution",
            "book",
        ]
        read_only_fields = [
            "copy_id",
            "user_id",
            "date_loan",
            "date_expected_devolution",
            "date_devolution",
        ]

    def get_book(self, instance: Loan):
        book = Book.objects.get(copies__id=instance.copy_id)
        book_serialized = BookSimpleSerializer(book)
        # import ipdb

        # ipdb.set_trace()

        return book_serialized.data
