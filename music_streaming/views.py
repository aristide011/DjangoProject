from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import  ListView,CreateView,UpdateView,DeleteView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Song,Playlist,Recommendations
from .forms import PlaylistForm
from django.urls import reverse_lazy
from django.db.models import Q


# Create your views here.
class SongListView(ListView): # class based generics
    model =Song
    template_name ='music_streaming/song_list.html'
    context_object_name ='songs'

 #La vista SongListView cerca per titolo di canzone quando l'utente inserisce una query di ricerca
    def get_queryset(self):
        query =self.request.GET.get('q')
        if query:
            return Song.objects.filter(Q(title__icontains=query)| Q(artist__icontains=query)| Q(album__icontains=query))
        return Song.objects.all()

class SongDetailView(DetailView):
        model=Song
        template_name='music_streaming/song_detail.html'
        context_object_name='song'
        

        def get_object(self):
            print(Song.objects.all())  # stampa tutti gli oggetti song nel database
            return super().get_object()


class SongCreateView(LoginRequiredMixin,CreateView):
       model=Song
       fields=['title','artist','album','genre','duration']
       template_name = 'music_streaming/song_create.html'

       def form_valid(self,form):# per aggiungere una logica personalizzata
          return super().form_valid(form)

       def get_success_url(self):
           return reverse_lazy('music_streaming:song_list')

class SongUpdateView(LoginRequiredMixin ,UpdateView) :
     model=Song
     fields=['title','artist','album','genre','duration']
     template_name='music_streaming/song_update.html'
     success_url = reverse_lazy('music_streaming:song_list')

     def form_valid(self,form):
         return super().form_valid(form)


class SongDeleteView(LoginRequiredMixin, DeleteView):
    model=Song
    template_name='music_streaming/song_confirm_delete.html'
    #reindirizza l'utente a song_list
    def get_success_url(self):
        return reverse_lazy('music_streaming:song_list')






class PlaylistCreateView(LoginRequiredMixin,CreateView):# solo utenti loggati possono creare playlist
    model= Playlist
    fields=['songs','name']
    template_name='music_streaming/playlist_create.html'
    success_url =reverse_lazy('playlist_list')

    def form_valid(self, form):
        form.instance.user = self.request.user  # associa la playlist all'utente loggato

        return super().form_valid(form)

class PlaylistListView(ListView):
        model = Playlist
        template_name = 'music_streaming/playlist_list.html'
        context_object_name = 'playlists'

        def get_queryset(self):
            query=self.request.GET.get('q')
            if query:
                return Playlist.objects.filter(Q(name__icontains=query)| Q(user__username__icontains=query))
            return Playlist.objects.all()


class PlaylistUpdateView(LoginRequiredMixin,UpdateView):#solo utenti loggati possono fare aggiornamenti
    model = Playlist
    fields=['name']
    template_name = 'music_streaming/playlist_update.html'
    success_url = reverse_lazy('music_streaming:playlist_list')


class PlaylistDeleteView(LoginRequiredMixin,DeleteView):
    model=Playlist
    template_name='music_streaming/playlist_confirm_delete.html'
    success_url=reverse_lazy('music_streaming:playlist_list') #ridirige dopo l'eliminazione





class RecommendationsCreateView(LoginRequiredMixin,CreateView) :
    model=Recommendations
    fields=['score','song']
    template_name='music_streaming/recommendation_create.html'
    success_url = reverse_lazy('music_streaming:recommendation_list')

    def form_valid(self,form):
        form.instance.user=self.request.user
        return super().form_valid(form) #per impostare automaticamente  il campo user sull'utente corrente

class  RecommendationsListView(ListView):
    model=Recommendations
    template_name='music_streaming/recommendation_list.html'

    def get_queryset(self):
        return Recommendations.objects.filter(user=self.request.user)

class RecommendationsUpdateView(LoginRequiredMixin,UpdateView):
    model=Recommendations
    fields=['score']
    template_name = 'music_streaming/recommendation_form.html'
    success_url = reverse_lazy('music_streaming:recommendation_list')

class RecommendationDeleteView(LoginRequiredMixin, DeleteView):
    model = Recommendations
    template_name = 'music_streaming/recommendation_confirm_delete.html'
    success_url = reverse_lazy('music_streaming:recommendation_list')


