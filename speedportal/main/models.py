from django.db import models
from django.contrib.auth.models import AbstractUser

class Game(models.Model):
    name = models.CharField(max_length=50, unique=True)
    steam_link = models.CharField(max_length=100, unique=True)
    icon = models.ImageField(upload_to='games_icons')
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name