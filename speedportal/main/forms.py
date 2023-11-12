from django import forms
from main.models import Game, Category, AllowedCategory, Run

class RunForm(forms.Form):
    game = forms.ModelChoiceField(queryset=Game.objects.all().order_by('name'), required=True)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True)
    runtime_ms = forms.IntegerField(required=True)
    video_link = forms.CharField(max_length=100, required=True)

    def game_category_is_valid(self):
        if not AllowedCategory.objects.filter(game=self.data['game'], category=self.data['category']).exists():
            self.errors['Игра/Категория: '] = 'Указанная категория недоступна для указанной игры'
            return False
        return True

    def runtime_is_valid(self):
        if int(self.data['runtime_ms']) <= 0:
            self.errors['Время рана: '] = 'Некорректное время рана'
            return False
        return True

    def is_valid(self):
        valid = super(RunForm, self).is_valid()
        game_category = self.game_category_is_valid()
        runtime = self.runtime_is_valid()
        return valid and game_category and runtime

    def save(self, user):
        Run.objects.create(game_category=AllowedCategory.objects.get(game=self.data['game'], category=self.data['category']),
                           user=user, runtime_ms=self.data['runtime_ms'], video_link=self.data['video_link'])