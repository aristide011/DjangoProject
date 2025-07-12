from django.contrib import admin
from .models import Song,Playlist,Recommendations



class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'album')

class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')

class RecommendationsAdmin(admin.ModelAdmin):
    list_display = ('song', 'user', 'created_at')

admin.site.register(Song, SongAdmin)
admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(Recommendations, RecommendationsAdmin)

