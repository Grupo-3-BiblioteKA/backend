# Generated by Django 4.1.7 on 2023-03-14 16:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("copies", "0004_loan_delete_loans_alter_copy_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="loan",
            name="date_expected_devolution",
            field=models.DateField(default=datetime.date(2023, 3, 29)),
        ),
    ]
