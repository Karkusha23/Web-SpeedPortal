from django import forms
from main.models import Game, Category, AllowedCategory, Run, Validation, Rejection
from users.models import User

class RunForm(forms.Form):
    game = forms.ModelChoiceField(queryset=Game.objects.all().order_by('name'), required=True)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True)
    runtime_hours = forms.IntegerField(required=True, initial=0, widget=forms.NumberInput(attrs={
        'placeholder': 'Часы'}))
    runtime_minutes = forms.IntegerField(required=True, initial=0, widget=forms.NumberInput(attrs={
        'placeholder': 'Минуты'}))
    runtime_seconds = forms.IntegerField(required=True, initial=0, widget=forms.NumberInput(attrs={
        'placeholder': 'Секунды'}))
    runtime_ms = forms.IntegerField(required=True, initial=0, widget=forms.NumberInput(attrs={
        'placeholder': 'Миллисекунды'}))
    video_link = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Ссылка на видео'}))

    def game_category_is_valid(self):
        if not AllowedCategory.objects.filter(game=self.data['game'], category=self.data['category']).exists():
            self.errors['Игра/Категория: '] = 'Указанная категория недоступна для указанной игры'
            return False
        return True

    def runtime_is_valid(self):
        hours = int(self.data['runtime_hours'])
        minutes = int(self.data['runtime_minutes'])
        seconds = int(self.data['runtime_seconds'])
        ms = int(self.data['runtime_ms'])
        valid = True
        if hours < 0 or hours > 500:
            self.errors['Часы: '] = 'Некорректное значение'
            valid = False
        if minutes < 0 or minutes > 60:
            self.errors['Минуты: '] = 'Некорректное значение'
            valid = False
        if seconds < 0 or seconds > 60:
            self.errors['Секунды: '] = 'Некорректное значение'
            valid = False
        if ms < 0 or ms > 1000:
            self.errors['Миллисекунды: '] = 'Некорректное значение'
            valid = False
        return valid

    def is_valid(self):
        valid = super(RunForm, self).is_valid()
        game_category = self.game_category_is_valid()
        runtime = self.runtime_is_valid()
        return valid and game_category and runtime

    def get_runtime_ms(self):
        hours = int(self.data['runtime_hours'])
        minutes = int(self.data['runtime_minutes'])
        seconds = int(self.data['runtime_seconds'])
        ms = int(self.data['runtime_ms'])
        return hours * 3600000 + minutes * 60000 + seconds * 1000 + ms

    def save(self, user):
        Run.objects.create(game_category=AllowedCategory.objects.get(game=self.data['game'], category=self.data['category']),
                           user=user, runtime_ms=self.get_runtime_ms(), video_link=self.data['video_link'])


class ValidationForm(forms.Form):
    validate_choice = forms.ChoiceField(choices=((1, 'Принять'), (2, 'Отклонить')), required=True)
    reject_reason = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Укажите причину отклонения забега'
    }))

    def save(self, run, moderator):
        if self.data['validate_choice'] == '1':
            run.is_validated = True
            points = run.get_points_for_run()
            user = User.objects.get(id=run.user_id)
            user.points += points
            user.save()
            Validation.objects.create(run=run, moderator=moderator, points=points)
        else:
            run.is_rejected = True
            Rejection.objects.create(run=run, moderator=moderator, reason=self.data['reject_reason'])
        run.save()