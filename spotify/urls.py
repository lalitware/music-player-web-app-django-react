from django.urls import path
from . import views

urlpatterns = [
    path('get-auth-url/', views.AuthURL.as_view(), name='get_auth_url'),
    path('redirect/', views.spotify_callback),
    path('check-update-auth/', views.CheckOrUpdateAuth.as_view(), name='check_update_auth'),
    path('get-current-song/', views.CurrentSong.as_view(), name='check_update_auth'),
    path('play-or-pause-song/', views.PlayOrPauseSong.as_view(), name='play_or_pause_song'),
    path('skip-to-next-song/', views.SkipToNextSong.as_view(), name='skip_to_next_song'),
]