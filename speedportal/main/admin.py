from django.contrib import admin
from main.models import Game, Category, AllowedCategory

admin.site.register(Game)
admin.site.register(Category)
admin.site.register(AllowedCategory)