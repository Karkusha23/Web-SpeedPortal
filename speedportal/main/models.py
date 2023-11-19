from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.text import slugify

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

    def get_leaderboard(self):
        return Run.objects.raw(f'SELECT * FROM ( '
                               f'SELECT DISTINCT ON (user_id) * FROM main_run '
                               f'WHERE game_category_id = {self.id} '
                               f'ORDER BY user_id, runtime_ms ASC '
                               f') ORDER BY runtime_ms ASC')


class Run(models.Model):
    from users.models import User

    game_category = models.ForeignKey(to=AllowedCategory, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    runtime_ms = models.PositiveIntegerField()
    video_link = models.CharField(max_length=100)
    time_uploaded = models.DateTimeField(default=timezone.now)
    is_validated = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'run'
        verbose_name_plural = 'runs'

    def __str__(self):
        return self.game_category.__str__() + ' ' + self.get_runtime_str()

    def get_runtime_str(self):
        hours = self.runtime_ms // 3600000
        minutes = (self.runtime_ms % 3600000) // 60000
        seconds = (self.runtime_ms % 60000) // 1000
        ms = self.runtime_ms % 1000
        result = ('0' if hours < 10 else '') + str(hours) + ':'
        result += ('0' if minutes < 10 else '') + str(minutes) + ':'
        result += ('0' if seconds < 10 else '') + str(seconds) + ':'
        result += ('0' if ms < 100 else '') + ('0' if ms < 10 else '') + str(ms)
        return result

    def get_place(self):
        return Run.objects.raw(f'SELECT 1 AS id, COUNT(*) FROM ( '
                               f'SELECT DISTINCT ON (user_id) * FROM main_run '
                               f'WHERE game_category_id = {self.game_category.id} AND runtime_ms < {self.runtime_ms} '
                               f'ORDER BY user_id, runtime_ms ASC) ')[0].count + 1

    def get_points_for_run(self):
        return max(10, 100 - self.get_place())


class Validation(models.Model):
    from users.models import Moderator

    run = models.OneToOneField(to=Run, on_delete=models.CASCADE, primary_key=True)
    moderator = models.ForeignKey(to=Moderator, on_delete=models.SET_NULL, null=True)
    points = models.PositiveIntegerField(default=0)
    time = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'validation'
        verbose_name_plural = 'validations'

    def __str__(self):
        return self.run.__str__()


class Rejection(models.Model):
    from users.models import Moderator

    run = models.OneToOneField(to=Run, on_delete=models.CASCADE, primary_key=True)
    moderator = models.ForeignKey(to=Moderator, on_delete=models.SET_NULL, null=True)
    reason = models.TextField()
    time = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'rejection'
        verbose_name_plural = 'rejections'

    def __str__(self):
        return self.run.__str__()


#def get_run_validation():
#    return Run.objects.raw('select main_run.id, main_run.runtime_ms, main_run.time_uploaded, main_run.user_id, '
#                           'main_game.name as game_name, main_category.name as category_name, '
#                           'main_validation.run_id as validated, main_refuse.run_id as refused '
#                           'from main_run '
#                           'left join main_allowedcategory on main_run.game_category_id = main_allowedcategory.id '
#                           'left join main_game on main_allowedcategory.game_id = main_game.id '
#                           'left join main_category on main_allowedcategory.category_id = main_category.id '
#                           'left join main_validation on main_run.id = main_validation.run_id '
#                           'left join main_refuse on main_run.id = main_refuse.run_id '
#                           'order by main_run.time_uploaded desc')