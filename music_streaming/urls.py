from django.urls import path
from .views import (SongListView,SongDetailView,SongCreateView,SongUpdateView,SongDeleteView,
                    PlaylistCreateView,PlaylistListView,PlaylistDeleteView,PlaylistUpdateView,
                    RecommendationsCreateView,RecommendationsListView,RecommendationsUpdateView,
                    RecommendationDeleteView)


app_name='music_streaming'

urlpatterns =[
    path('song/',SongListView.as_view(),name ='song_list'),
    path('song/<int:pk>/',SongDetailView.as_view(),name ='song_detail'),
    path('song/create/',SongCreateView.as_view(), name='song_create'),
    path('song/update/<int:pk>/',SongUpdateView.as_view(), name='song_update'),
    path('song/delete/<int:pk>/',SongDeleteView.as_view(),name='song_confirm_delete'),
    path('playlist/',PlaylistListView.as_view(),name='playlist_list'),
    path('playlist/create',PlaylistCreateView.as_view(),name='playlist_create'),
    path('playlist/delete/<int:pk>/',PlaylistDeleteView.as_view(),name='playlist_confirm_delete'),
    path('playlist/update/<int:pk>/',PlaylistUpdateView.as_view(),name='playlist_update'),
    path('recommendations/',RecommendationsListView.as_view() ,name='recommendation_list'),
    path('recommendations/create',RecommendationsCreateView.as_view(), name='recommendation_create'),
    path('recommendations/update/<int:pk>/',RecommendationsUpdateView.as_view(), name='recommendation_form'),
    path('recommendations/delete/<int:pk>/',RecommendationDeleteView.as_view(),name='recommendation_confirm_delete'),













































































































]