from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from users.models import User


class Command(BaseCommand):
    help = "Create users for test"

    def handle(self, *args, **kwargs):
        users_data = [
            {
                "username": "anderson",
                "email": "anderson@mail.com",
                "password": make_password("1234"),
            },
            {
                "username": "gabriela",
                "email": "gabriela@mail.com",
                "password": make_password("1234"),
            },
            {
                "username": "enrico",
                "email": "enrico@mail.com",
                "password": make_password("1234"),
            },
            {
                "username": "andressa",
                "email": "andressa@mail.com",
                "password": make_password("1234"),
            },
        ]

        users_obj = [User(**user) for user in users_data]

        User.objects.bulk_create(users_obj, ignore_conflicts=True)

        for user in users_data:
            self.stdout.write(f"User `{user['username']}` successfully created!")
