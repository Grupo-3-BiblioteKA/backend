from rest_framework import serializers
from .models import Book
from copies.models import Copy


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "name", "author", "year", "sinopsy", "pages"]

    def create(self, validated_data):
        print(validated_data)

        copies = validated_data.pop("copies")

        new_book = Book.objects.create(**validated_data)

        for _ in range(copies):
            copie = Copy.objects.create(book_id=new_book.id)

        # import ipdb

        # ipdb.set_trace()
        return new_book
