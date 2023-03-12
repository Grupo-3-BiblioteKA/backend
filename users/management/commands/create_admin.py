from django.core.management.base import BaseCommand, CommandParser
from users.models import User

from django.core.management import base


class Command(BaseCommand):
    help = "Create a superuser"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--username", type=str, help="Indicates the username for superuser"
        )

        parser.add_argument(
            "--password", type=str, help="Indicates the password for superuser"
        )

        parser.add_argument(
            "--email", type=str, help="Indicates the email for superuser"
        )

    def handle(self, *args, **kwargs):
        username = kwargs["username"] or "admin"
        password = kwargs["password"] or "admin1234"
        email = kwargs["email"] or username + "@example.com"

        check_username = User.objects.filter(username=username)

        if check_username:
            raise base.CommandError(f"Username `{username}` already taken.")

        check_email = User.objects.filter(email=email)

        if check_email:
            raise base.CommandError(f"Email `{email}` already taken.")

        User.objects.create_superuser(username=username, password=password, email=email)

        self.stdout.write(f"Admin `{username}` successfully created!")
