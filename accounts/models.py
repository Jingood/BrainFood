import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=50, unique=True)
    nickname = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=254, unique=True)

    REQUIRED_FIELDS = ["email", "nickname"]
