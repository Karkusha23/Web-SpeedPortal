from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from users.models import User

class Game(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    steam_link = models.CharField(max_length=100, unique=True)
    icon = models.ImageField(upload_to='games_icons', default='games_icons/default_game_icon.jpg')
    banner = models.ImageField(upload_to='games_banners', default='games_banners/default_game_banner.jpg')
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'game'
        verbose_name_plural = 'games'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Game, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_allowed_categories(self):
        return AllowedCategory.objects.filter(game=self)


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class AllowedCategory(models.Model):
    game = models.ForeignKey(to=Game, on_delete=models.CASCADE)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)
    extra_description = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = (('game', 'category'),)
        verbose_name = 'allowed category'
        verbose_name_plural = 'allowed categories'

    def __str__(self):
        return self.game.name + ' ' + self.category.name


class Run(models.Model):
    game_category = models.ForeignKey(to=AllowedCategory, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    runtime_ms = models.PositiveIntegerField()
    video_link = models.CharField(max_length=100)
    time_upoaded = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'run'
        verbose_name_plural = 'runs'

    def __str__(self):
        return __str__(self.game_category) + ' ' + self.runtime_ms