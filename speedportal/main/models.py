from django.db import models
from django.contrib.auth.models import AbstractUser

class Game(models.Model):
    name = models.CharField(max_length=50, unique=True)
    steam_link = models.CharField(max_length=100, unique=True)
    icon = models.ImageField(upload_to='games_icons', default='games_icons/default_game_icon.jpg')
    banner = models.ImageField(upload_to='games_banners', default='games_banners/default_game_banner.jpg')
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'game'
        verbose_name_plural = 'games'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class AllowedCategory(models.Model):
    game = models.ForeignKey(to=Game, on_delete=models.CASCADE)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('game', 'category'),)
        verbose_name = 'allowed category'
        verbose_name_plural = 'allowed categories'

    def __str__(self):
        return self.game.name + ' ' + self.category.name