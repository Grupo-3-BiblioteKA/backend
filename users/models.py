from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	email = models.EmailField(max_length=254, unique=True)
	date_unlock = models.DateField(null=True)