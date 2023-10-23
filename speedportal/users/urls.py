from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'users'

urlpatterns = [
    path('login', views.login, name='login'),
    path('registration', views.registration, name='registration'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)