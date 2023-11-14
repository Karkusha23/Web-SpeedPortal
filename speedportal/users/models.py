from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy
from .managers import CustomUserManager
from django.utils.text import slugify

class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(gettext_lazy('Адрес электронной почты'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
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
        return Run.objects.filter(user=self).order_by('-time_uploaded')

    def get_unseen_runs(self):
        from main.models import Run
        return Run.objects.filter(user=self).filter(is_validated=False, is_rejected=False).order_by('-time_uploaded')

    def get_validated_runs(self):
        from main.models import Run
        return Run.objects.filter(user=self).filter(is_validated=True).order_by('-time_uploaded')

    def get_rejected_runs(self):
        from main.models import Run
        return Run.objects.filter(user=self).filter(is_rejected=True).order_by('-time_uploaded')

    def get_moderator(self, game):
        return Moderator.objects.get(user=self, game=game)


class Moderator(models.Model):
    from main.models import Game

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    game = models.ForeignKey(to=Game, on_delete=models.CASCADE)
    can_make_moderators = models.BooleanField(default=False)
    can_add_categories = models.BooleanField(default=False)
    can_approve_runs = models.BooleanField(default=False)
    can_ban = models.BooleanField(default=False)

    class Meta:
        unique_together = (('user', 'game'),)
        verbose_name = 'moderator'
        verbose_name_plural = 'moderators'

    def __str__(self):
        return self.user.__str__() + ': ' + self.game.__str__()