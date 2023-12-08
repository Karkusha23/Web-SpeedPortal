from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('games/', views.all_games, name='all_games'),
    path('game-<slug:game_slug>/', views.game, name='game'),
    path('run/upload/', views.run_upload, name='run_upload'),
    path('run/<int:run_id>/', views.run, name='run'),
    path('run/-<slug:user_slug>/', views.user_runs, name='user_runs'),
    path('run/unvalidated/', views.unvalidated_runs, name='unvalidated_runs'),
    path('moderation/', views.moderation, name='moderation'),
    path('game-<slug:game_slug>/<slug:category_slug>/', views.leaderboard, name='leaderboard')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)