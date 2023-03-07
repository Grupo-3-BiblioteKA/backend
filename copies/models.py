from django.db import models


class StatusCopy(models.TextChoices):
    Available = "Available"
    Borrowed = "Borrowed"


class Copy(models.Model):
    status = models.CharField(
        max_length=50, choices=StatusCopy.choices, default=StatusCopy.Available
    )

    book = models.ForeignKey(
        "books.Book", on_delete=models.CASCADE, related_name="copies"
    )

    user = models.ManyToManyField(
        "users.User", through="copies.Loans", related_name="copies"
    )


class Loans(models.Model):
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="loan_user"
    )

    copy = models.ForeignKey(
        "copies.Copy", on_delete=models.CASCADE, related_name="loan_copy"
    )
    date_loan = models.DateField(auto_now_add=True)
    date_expected_devolution = models.DateField(null=True)
    date_devolution = models.DateField(null=True)
