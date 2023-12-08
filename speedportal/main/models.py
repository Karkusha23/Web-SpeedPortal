from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.text import slugify
from django.db.models import Subquery

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
        runs = Run.objects.filter(game_category=self, is_validated=True, user__is_banned=False).order_by('user', 'runtime_ms').distinct('user')
        return Run.objects.filter(id__in=Subquery(runs.values('id'))).order_by('runtime_ms').prefetch_related('user', 'game_category', 'game_category__game', 'game_category__category')


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
        return Run.objects.filter(game_category=self.game_category, is_validated=True, user__is_banned=False, runtime_ms__lt=self.runtime_ms).order_by('user', 'runtime_ms').distinct('user').count() + 1

    def get_points_for_run(self):
        return max(10, 100 - self.get_place())

    def get_comments(self):
        return Comment.objects.filter(run=self).order_by('-parent_comment__time', 'time').prefetch_related('user', 'parent_comment')


class Validation(models.Model):
    from users.models import Moderator

    run = models.OneToOneField(to=Run, on_delete=models.CASCADE, primary_key=True, related_name='validation')
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

    run = models.OneToOneField(to=Run, on_delete=models.CASCADE, primary_key=True, related_name='rejection')
    moderator = models.ForeignKey(to=Moderator, on_delete=models.SET_NULL, null=True)
    reason = models.TextField()
    time = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'rejection'
        verbose_name_plural = 'rejections'

    def __str__(self):
        return self.run.__str__()

    def get_short_text(self):
        return self.reason[:15] + '...' if len(self.reason) > 15 else self.reason


class Comment(models.Model):
    from users.models import User

    run = models.ForeignKey(to=Run, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    parent_comment = models.ForeignKey(to='self', on_delete=models.CASCADE, null=True)
    comment_text = models.TextField()
    time = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'comments'

    def save(self, *args, **kwargs):
        super(Comment, self).save(*args, **kwargs)
        if not self.parent_comment:
            comment = Comment.objects.get(id=self.id)
            comment.parent_comment = comment
            comment.save()

    def __str__(self):
        return self.run.__str__()


class Report(models.Model):
    from users.models import User

    run = models.ForeignKey(to=Run, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    report_text = models.TextField()
    time = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'report'
        verbose_name_plural = 'reports'

    def __str__(self):
        return self.run.__str__()

    def get_short_text(self):
        return self.report_text[:15] + '...' if len(self.report_text) > 15 else self.report_text