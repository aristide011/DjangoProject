from django.test import TestCase
from music_streaming.models import Song,Playlist,Recommendations
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import PlaylistForm,RecommendationForm


# Create your tests here.

#test sui modelli dell'app
class SongModelTest(TestCase):
    def test_create_song(self):
        song= Song.objects.create(title="Test Song" , artist="Test Artist",album="Test Album",duration=180,genre="Test Genre")

        self.assertEqual(song.title,"Test Song")
        self.assertEqual(song.artist,"Test Artist")
        self.assertEqual(song.album,"Test Album")
        self.assertEqual(song.duration,180)
        self.assertEqual(song.genre,"Test Genre")

    def test_str_representation(self):
        song=Song.objects.create(title="Test Song", artist="Test Artist", album="Test Album", duration=180, genre="Test Genre")
        self.assertEqual(str(song),"Test Song di Test Artist ")




class PlaylistModelTest(TestCase):
    def setUp(self):
        self.user=get_user_model().objects.create_user(username="testuser" ,password="testpassword",first_name="Test",last_name="User",email="testuser@example.com")
    def test_create_playlist(self):
        playlist=Playlist.objects.create(user=self.user,name="Test Playlist")

        self.assertEqual(playlist.user,self.user)
        self.assertEqual(playlist.name,"Test Playlist")

    def test_str_representation(self):
        playlist=Playlist.objects.create(user=self.user,name="Test Playlist")
        self.assertEqual(str(playlist),f"playlist'Test Playlist' di {self.user.first_name}{self.user.last_name}" )


class RecommendationsModel(TestCase):
    def setUp(self):
        self.user=get_user_model().objects.create_user(username="testuser",password="testpassword",first_name="Test", last_name="User",email="testuser@example.com")
        self.song=Song.objects.create(title="Test Song",artist="test Artist",album="Test Album",duration=180,genre="Test Genre")

    def test_create_recommendations(self):
        recommendation=Recommendations.objects.create(user=self.user,song=self.song)

        self.assertEqual(recommendation.user,self.user)
        self.assertEqual(recommendation.song,self.song)

    def test_str_representation(self):
        recommendation=Recommendations.objects.create(user=self.user,song=self.song)
        self.assertEqual(str(recommendation),f"Raccomandazione per {self.song.title} - {self.user.first_name} {self.user.last_name}")

#test sulle viste dell'app

class SongListViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response=self.client.get('/music_streaming/song/')
        self.assertEqual(response.status_code,200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('music_streaming:song_list'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'music_streaming/song_list.html')


class SongDetailViewTest(TestCase):
    def setUp(self):
        self.user=get_user_model().objects.create_user(username='testuser',email= 'test@example.com', password='testpassword')
        self.song = Song.objects.create(title='Test Song', artist='Test Artist', duration=180)

    def test_view_url_exists_at_desired_location(self):
        print(self.song.pk)
        self.client.force_login(self.user)
        response = self.client.get(reverse('music_streaming:song_detail', args=[self.song.pk]))
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('music_streaming:song_detail', args=[self.song.pk]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('music_streaming:song_detail', args=[self.song.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'music_streaming/song_detail.html')

    def test_view_returns_correct_object(self):
        response = self.client.get(reverse('music_streaming:song_detail', args=[self.song.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['song'].pk, self.song.pk)
        self.assertEqual(response.context['song'].title, self.song.title)
        self.assertEqual(response.context['song'].artist, self.song.artist)

    def test_view_returns_404_for_nonexistent_song(self):
        response = self.client.get(reverse('music_streaming:song_detail', args=[999]))
        self.assertEqual(response.status_code, 404)


# per le viste di song ,aggiornamento,creazione e cancellazione
class SongCreateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword',email="testuser@example.com")
        self.client.force_login(self.user)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('music_streaming:song_create'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('music_streaming:song_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'music_streaming/song_create.html')

    def test_create_song(self):
        data = {'title': 'Test Song', 'artist': 'Test Artist', 'album': 'Test Album','duration':'180','genre':'Test Genre'}
        response = self.client.post(reverse('music_streaming:song_create'),data)
        self.assertRedirects(response,reverse('music_streaming:song_list'))
        self.assertEqual(Song.objects.count(), 1)



class SongUpdateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword',email="testuser@example.com")
        self.client.force_login(self.user)
        self.song = Song.objects.create(title='Test Song', artist='Test Artist', album='Test Album',duration=180,genre='Test Genre')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('music_streaming:song_update', kwargs={'pk': self.song.pk}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('music_streaming:song_update', kwargs={'pk': self.song.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'music_streaming/song_update.html')

    def test_update_song(self):
        data = {'title': 'Updated Test Song','artist': 'Test Artist','album': 'Test Album','duration': 180,'genre': 'Test Genre'}
        response = self.client.post(reverse('music_streaming:song_update', kwargs={'pk': self.song.pk}), data)
        self.assertEqual(response.status_code, 302)
        self.song.refresh_from_db()
        self.assertEqual(self.song.title, 'Updated Test Song')

class SongDeleteViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword',email="testuser@example.com")
        self.client.force_login(self.user)
        self.song = Song.objects.create(title='Test Song', artist='Test Artist', album='Test Album',duration=180,genre='Test Genre')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('music_streaming:song_confirm_delete', kwargs={'pk': self.song.pk}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('music_streaming:song_confirm_delete', kwargs={'pk': self.song.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'music_streaming/song_confirm_delete.html')

    def test_delete_song(self):
        response = self.client.post(reverse('music_streaming:song_confirm_delete', kwargs={'pk': self.song.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Song.objects.count(), 0)


#per le playlist

class PlaylistCreateViewTest(TestCase) :
    def setUp (self):
        self.user=get_user_model().objects.create_user(username='testuser',password='testpassword',email="testuser@example.com")
        self.client.force_login(self.user)

    def test_view_url_exists_at_desired_location(self):
        response=self.client.get(reverse('music_streaming:playlist_create'))
        self.assertEqual(response.status_code,200)

    def test_view_uses_correct_template(self):
        response=self.client.get(reverse('music_streaming:playlist_create'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'music_streaming/playlist_create.html')

class PlaylistListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword',email="testuser@example.com")
        self.client.force_login(self.user)
        self.playlist1 = Playlist.objects.create(name='Test Playlist 1',user=self.user)
        self.playlist2 = Playlist.objects.create(name='Test Playlist 2',user=self.user)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('music_streaming:playlist_list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('music_streaming:playlist_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'music_streaming/playlist_list.html')

    def test_view_displays_playlists(self):
        response = self.client.get(reverse('music_streaming:playlist_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.playlist1.name)
        self.assertContains(response, self.playlist2.name)

class PlaylistUpdateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser',email='testuser@example.com', password='password')
        self.client.force_login(self.user)
        self.playlist = Playlist.objects.create(name='Test Playlist',user=self.user)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('music_streaming:playlist_update', kwargs={'pk': self.playlist.pk}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('music_streaming:playlist_update', kwargs={'pk': self.playlist.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'music_streaming/playlist_update.html')

    def test_update_playlist(self):
        data = {'name': 'Updated Test Playlist'}
        response = self.client.post(reverse('music_streaming:playlist_update', kwargs={'pk': self.playlist.pk}), data)
        self.assertEqual(response.status_code, 302)
        self.playlist.refresh_from_db()
        self.assertEqual(self.playlist.name, 'Updated Test Playlist')

        self.client.force_login(self.user)
        response = self.client.post(reverse('music_streaming:playlist_update', args=[self.playlist.pk]),
                                    {'name': 'New Name'})
        self.assertEqual(response.status_code, 302)

class PlaylistDeleteViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser',email='test@example.com',password='testpassword')
        self.client.force_login(self.user)
        self.playlist = Playlist.objects.create(name='Test Playlist',user=self.user)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('music_streaming:playlist_confirm_delete', kwargs={'pk': self.playlist.pk}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('music_streaming:playlist_confirm_delete', kwargs={'pk': self.playlist.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'music_streaming/playlist_confirm_delete.html')

    def test_delete_playlist(self):
        response = self.client.post(reverse('music_streaming:playlist_confirm_delete', kwargs={'pk': self.playlist.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Playlist.objects.count(), 0)



#per le raccomandazioni
class RecommendationsListViewTest(TestCase):
    def setUp(self):
        self.user=get_user_model().objects.create_user(username='testuser',password='testpassword',email='testuser@example.com')
        self.client.force_login(self.user)

    def test_view_url_exists_at_desired_location(self):
        response=self.client.get(reverse('music_streaming:recommendation_list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response= self.client.get(reverse('music_streaming:recommendation_list'))
        self.assertEqual(response.status_code,200)

        self.assertTemplateUsed(response,'music_streaming/recommendation_list.html')

class RecommendationsCreateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', email='test@example.com',password='password')
        self.client.force_login(self.user)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('music_streaming:recommendation_create'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('music_streaming:recommendation_create'))
        self.assertTemplateUsed(response, 'music_streaming/recommendation_create.html')

    def test_create_recommendation(self):
        song=Song.objects.create(title='title of song',artist='artist of song',duration= 180)
        response = self.client.post(reverse('music_streaming:recommendation_create'), {'score': 5,'song':song.id})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Recommendations.objects.count(), 1)



class RecommendationsUpdateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', email='test@example.com',password= 'password')
        self.client.force_login(self.user)
        self.song = Song.objects.create(title='title of song', artist='artist of song', duration=180)
        self.recommendation = Recommendations.objects.create(user=self.user, score=5, song=self.song)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('music_streaming:recommendation_form', args=[self.recommendation.pk]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('music_streaming:recommendation_form', args=[self.recommendation.pk]))
        self.assertTemplateUsed(response, 'music_streaming/recommendation_form.html')

    def test_update_recommendation(self):
        response = self.client.post(reverse('music_streaming:recommendation_form', args=[self.recommendation.pk]), {
            'score': 4        })
        self.assertEqual(response.status_code, 302)
        self.recommendation.refresh_from_db()
        self.assertEqual(self.recommendation.score, 4)


class RecommendationDeleteViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', email='test@example.com', password='password')
        self.client.force_login(self.user)
        self.song = Song.objects.create(title='Test Song', artist='Test Artist',duration=180)
        self.recommendation = Recommendations.objects.create(user=self.user, score=5,song=self.song)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('music_streaming:recommendation_confirm_delete', args=[self.recommendation.pk]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('music_streaming:recommendation_confirm_delete', args=[self.recommendation.pk]))
        self.assertTemplateUsed(response, 'music_streaming/recommendation_confirm_delete.html')

    def test_delete_recommendation(self):
        response = self.client.post(reverse('music_streaming:recommendation_confirm_delete', args=[self.recommendation.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Recommendations.objects.count(), 0)


#Test sui form
class PlaylistFormTest(TestCase):
    def test_form_is_valid(self):
        song = Song.objects.create(title='Test Song', artist='Test Artist', duration=180)
        data = {'name': 'Test Playlist', 'songs': [song.pk]}
        form = PlaylistForm(data)
        self.assertTrue(form.is_valid())

    def test_form_is_not_valid_without_name(self):
        song = Song.objects.create(title='Test Song', artist='Test Artist', duration=180)
        data = {'songs': [song.pk]}
        form = PlaylistForm(data)
        self.assertFalse(form.is_valid())

    def test_form_is_not_valid_without_songs(self):
        data = {'name': 'Test Playlist'}
        form = PlaylistForm(data)
        self.assertFalse(form.is_valid())

class RecommendationFormTest(TestCase):
    def test_form_is_valid(self):
        song = Song.objects.create(title='Test Song', artist='Test Artist', duration=180)
        data = {'score': 5, 'song': song.pk}
        form = RecommendationForm(data)
        self.assertTrue(form.is_valid())

    def test_form_is_not_valid_without_score(self):
        song = Song.objects.create(title='Test Song', artist='Test Artist', duration=180)
        data = {'song': song.pk}
        form = RecommendationForm(data)
        self.assertFalse(form.is_valid())

    def test_form_is_not_valid_without_song(self):
        data = {'score': 5}
        form = RecommendationForm(data)
        self.assertFalse(form.is_valid())

    def test_form_is_not_valid_with_invalid_score(self):
        song = Song.objects.create(title='Test Song', artist='Test Artist', duration=180)
        data = {'score': 6, 'song': song.pk}
        form = RecommendationForm(data)
        self.assertFalse(form.is_valid())
