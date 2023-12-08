from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy
from .managers import CustomUserManager
from django.utils.text import slugify
from django.db.models import Subquery

class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(gettext_lazy('Адрес электронной почты'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_banned = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    username = models.CharField(gettext_lazy('Имя пользователя'), max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    pfp = models.ImageField(upload_to='pfps', default='pfps/def_pfp.jpg')
    points = models.PositiveIntegerField(default=0)
    about = models.TextField(blank=True, default='')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.username

    def get_runs(self):
        from main.models import Run
        return Run.objects.filter(user=self).order_by('-time_uploaded').prefetch_related('game_category', 'game_category__game', 'game_category__category')

    def get_unseen_runs(self):
        from main.models import Run
        return Run.objects.filter(user=self, is_validated=False, is_rejected=False).order_by('-time_uploaded').prefetch_related('game_category', 'game_category__game', 'game_category__category')

    def get_validated_runs(self):
        from main.models import Run
        return Run.objects.filter(user=self, is_validated=True).order_by('-time_uploaded').prefetch_related('game_category', 'game_category__game', 'game_category__category')

    def get_rejected_runs(self):
        from main.models import Run
        return Run.objects.filter(user=self, is_rejected=True).order_by('-time_uploaded').prefetch_related('rejection', 'game_category', 'game_category__game', 'game_category__category')

    def has_unvalidated_runs(self):
        from main.models import Run
        return Run.objects.filter(user=self, is_validated=False).exists()

    def has_unseen_runs(self):
        from main.models import Run
        return Run.objects.filter(user=self, is_validated=False, is_rejected=False).exists()

    def has_rejected_runs(self):
        from main.models import Run
        return Run.objects.filter(user=self, is_rejected=True).exists()

    def is_moderator(self):
        return Moderator.objects.filter(user=self).exists()

    def get_moderators(self):
        return Moderator.objects.filter(user=self)

    def get_ban_reason(self):
        if self.is_banned:
            return Ban.objects.get(user=self).reason

    def get_relevant_reports_for(self, other_user):
        from main.models import Report
        games = Moderator.objects.filter(user=other_user, can_ban=True).values('game')
        return Report.objects.filter(run__user=self, run__game_category__game__in=Subquery(games)).exclude(user=other_user).order_by('time')


class Moderator(models.Model):
    from main.models import Game

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    game = models.ForeignKey(to=Game, on_delete=models.CASCADE)
    can_make_moderators = models.BooleanField(default=False)
    can_add_categories = models.BooleanField(default=False)
    can_validate_runs = models.BooleanField(default=False)
    can_ban = models.BooleanField(default=False)

    class Meta:
        unique_together = (('user', 'game'),)
        verbose_name = 'moderator'
        verbose_name_plural = 'moderators'

    def __str__(self):
        return self.user.__str__() + ': ' + self.game.__str__()

    def get_unseen_runs(self):
        from main.models import Run
        return Run.objects.filter(game_category__game=self.game, is_validated=False, is_rejected=False).exclude(user=self.user).order_by('time_uploaded')

    def get_reports(self):
        from main.models import Report
        return Report.objects.filter(run__game_category__game=self.game, run__user__is_banned=False).exclude(run__user=self.user).exclude(user=self.user).order_by('time')


class Ban(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, primary_key=True)
    moderator = models.ForeignKey(to=Moderator, on_delete=models.SET_NULL, null=True)
    reason = models.TextField()
    time = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'ban'
        verbose_name_plural = 'bans'

    def __str__(self):
        return self.user.__str__()