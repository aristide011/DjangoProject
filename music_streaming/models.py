from django.db import models
from django.conf import settings

# Create your models
class Song(models.Model):
    title=models.CharField(max_length=200,null=False)
    artist=models.CharField(max_length=100,null=False)
    album =models.CharField(max_length=200,null=False)
    duration=models.IntegerField()
    genre=models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title} di {self.artist} "

class Playlist(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL ,on_delete=models.CASCADE,null=True)#relazione many-to-one tra il
    songs=models.ManyToManyField(Song,related_name='playlists')   #in questo caso una playlist può avere molti songe viceversa
    name=models.CharField(max_length=200)

    def __str__(self):
        return f"playlist'{self.name}' di {self.user.first_name}{self.user.last_name}"

class Recommendations(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    song=models.ForeignKey(Song, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)


    def __str__(self):
        return f"Raccomandazione per {self.song.title} - {self.user.first_name} { self.user.last_name}"


