from django.contrib import admin
from main.models import Game, Category, AllowedCategory, Run, Validation, Rejection

class GameAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Game, GameAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(AllowedCategory)
admin.site.register(Run)
admin.site.register(Validation)
admin.site.register(Rejection)