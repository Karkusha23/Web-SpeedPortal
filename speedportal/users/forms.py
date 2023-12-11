from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django import forms
from django.db.models import Subquery
from .models import User, Moderator, Ban
from main.models import Game

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Введите адрес электронной почты'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Введите имя пользователя'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Введите пароль'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Подтведите пароль'
    }))

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')


class UserProfileForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={}))
    username = forms.CharField(widget=forms.TextInput(attrs={}))
    pfp = forms.ImageField(widget=forms.FileInput(attrs={}), required=False)
    about = forms.CharField(widget=forms.TextInput(attrs={}), required=False)

    class Meta:
        model = User
        fields = ('email', 'username', 'pfp', 'about')


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Введите адрес электронной почты'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Введите пароль'
    }))

    class Meta:
        model = User
        fields = ('username', 'password')


class BanForm(forms.Form):
    ban_reason = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Укажите причину бана'
    }))

    def save(self, user, moderator):
        Ban.objects.create(user=user, moderator=moderator, reason=self.data['ban_reason'])
        user.is_banned = True
        user.save()


class ModeratorForm(forms.Form):
    game = forms.ModelChoiceField(queryset=Game.objects.none(), required=True)
    can_make_moderators = forms.BooleanField(initial=False, required=False)
    can_add_categories = forms.BooleanField(initial=False, required=False)
    can_validate_runs = forms.BooleanField(initial=False, required=False)
    can_ban = forms.BooleanField(initial=False, required=False)

    def __init__(self, game_values=Game.objects.all().values('id'), *args, **kwargs):
        super(ModeratorForm, self).__init__(*args, **kwargs)
        if game_values:
            self.fields['game'].queryset = Game.objects.filter(id__in=Subquery(game_values)).order_by('name')

    def save(self, user):
        print(self.data.get('can_validate_runs', None))
        Moderator.objects.create(user=user, game=Game.objects.get(id=self.data['game']),
                         can_make_moderators=(self.data.get('can_make_moderators', None) is not None),
                         can_add_categories=(self.data.get('can_add_categories', None) is not None),
                         can_validate_runs=(self.data.get('can_validate_runs', None) is not None),
                         can_ban=(self.data.get('can_ban', None) is not None))