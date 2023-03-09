# Generated by Django 4.1.7 on 2023-03-09 21:18


import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Copy",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("Available", "Available"), ("Borrowed", "Borrowed")],
                        default="Available",
                        max_length=50,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Loans",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_loan", models.DateField(auto_now_add=True)),
                (
                    "date_expected_devolution",
                    models.DateField(default=datetime.date(2023, 3, 24)),
                ),
                ("date_devolution", models.DateField(null=True)),
                (
                    "copy",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="loan_copy",
                        to="copies.copy",
                    ),
                ),
            ],
        ),
    ]
