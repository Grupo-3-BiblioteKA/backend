from rest_framework import serializers
from .models import Book, Follow
from copies.models import Copy


class BookSerializer(serializers.ModelSerializer):
    copies = serializers.IntegerField(write_only=True, default=1)
    quantity_of_copies = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Book
        fields = [
            "id",
            "name",
            "author",
            "year",
            "sinopsy",
            "pages",
            "copies",
            "quantity_of_copies",
        ]

    def create(self, validated_data):
        copies = validated_data.pop("copies")

        new_book = Book.objects.create(**validated_data)

        for _ in range(copies):
            Copy.objects.create(book_id=new_book.id)

        return new_book

    def get_quantity_of_copies(self, book: Book):
        total_copies = Copy.objects.filter(book_id=book.id)
        copies_available = total_copies.filter(status="Available")
        return {
            "total_copies": len(total_copies),
            "copies_available": len(copies_available),
        }


class FollowSerializer(serializers.ModelSerializer):
    book = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ["id", "book", "user"]

    def get_book(self, validated_data: dict):
        book = validated_data.book.id
        return book

    def get_user(self, validated_data: dict):
        user = validated_data.user.id
        return user


class BookSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            "id",
            "name",
            "author",
            "year",
            "pages",
        ]
        read_only_fields = [
            "id",
            "name",
            "author",
            "year",
            "pages",
        ]
