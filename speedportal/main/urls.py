from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('allgames/', views.all_games, name='all_games'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)