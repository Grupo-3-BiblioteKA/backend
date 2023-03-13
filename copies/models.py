from django.db import models
from datetime import timedelta
from django.utils import timezone


class StatusCopy(models.TextChoices):
    Available = "Available"
    Borrowed = "Borrowed"


def get_date_expected_devolution():
    date_now = timezone.now().date()
    dead_line = timedelta(days=15)
    date_sum = date_now + dead_line
    if date_sum.weekday() == 5:
        return date_sum + timedelta(days=2)
    elif date_sum.weekday() == 6:
        return date_sum + timedelta(days=1)
    return date_sum


class Copy(models.Model):
    status = models.CharField(
        max_length=50, choices=StatusCopy.choices, default=StatusCopy.Available
    )

    book = models.ForeignKey(
        "books.Book", on_delete=models.CASCADE, related_name="copies"
    )

    user = models.ManyToManyField(
        "users.User", through="copies.Loan", related_name="copies"
    )


class Loan(models.Model):
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="loan_user"
    )

    copy = models.ForeignKey(
        "copies.Copy", on_delete=models.CASCADE, related_name="loan_copy"
    )
    date_loan = models.DateField(auto_now_add=True)

    date_expected_devolution = models.DateField(default=get_date_expected_devolution())

    date_devolution = models.DateField(null=True)
