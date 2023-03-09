from rest_framework import serializers
from .models import Copy, Loans

from books.serializers import BookSerializer


class CopySerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

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
    class Meta:
        model = Loans
        fields = [
            "id",
            "copy_id",
            "user_id",
            "date_loan",
            "date_expected_devolution",
            "date_devolution",
        ]
        read_only_fields = [
            "copy_id",
            "user_id",
            "date_loan",
            "date_expected_devolution",
            "date_devolution",
        ]
