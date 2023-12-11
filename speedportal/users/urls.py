from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('user-<slug:user_slug>/', views.profile, name='profile'),
    path('user-<slug:user_slug>/ban/', views.profile_ban_post, name='profile_ban_post'),
    path('user-<slug:user_slug>/moderator/', views.profile_moderator_post, name='profile_moderator_post'),
    path('profilechange/', views.profile_change, name='profile_change'),
    path('logout/', views.logout, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)