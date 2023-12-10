from django.contrib import admin
from main.models import Game, Category, AllowedCategory, Run, Validation, Rejection, Comment, Report

class GameAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class AllowedCategoryAdmin(admin.ModelAdmin):
    list_display = ('game', 'category')
    list_filter = ('game', 'category')
    search_fields = ('game', 'category')

class RunAdmin(admin.ModelAdmin):
    list_display = ('user', 'game_category', 'runtime_ms')
    list_filter = ('user', 'game_category')
    search_fields = ('user', 'game_category')

admin.site.register(Game, GameAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(AllowedCategory, AllowedCategoryAdmin)
admin.site.register(Run, RunAdmin)
admin.site.register(Validation)
admin.site.register(Rejection)
admin.site.register(Comment)
admin.site.register(Report)