from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy
from .managers import CustomUserManager
from django.utils.text import slugify
import main.models

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
        return self.email

    def get_runs(self):
        return main.models.Run.objects.filter(user=self).order_by('-time_upoaded')