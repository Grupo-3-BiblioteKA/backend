from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    def create(self, validate_data: dict):
        return User.objects.create_user(**validate_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

            if key == "password":
                instance.set_password(value)

        instance.save()
        return instance

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
            "is_superuser",
            "date_unlock",
        ]
        extra_kwargs = {"password": {"write_only": True}}


class UserSerializerStatus(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["date_unlock"]
        read_only_fields = ["date_unlock"]
