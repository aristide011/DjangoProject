from django import forms
from .models import Playlist ,Song,Recommendations

class PlaylistForm(forms.ModelForm):
    name=forms.CharField(label="Nome della playlist", max_length=200)
    songs=forms.ModelMultipleChoiceField( label="Canzoni",queryset=Song.objects.all() , widget=forms.CheckboxSelectMultiple ) #Selezionare multiple canzoni usando checkbox


    class Meta:
        model =Playlist
        fields=['name','songs']

    def __init__(self,*args ,**kwargs):
        super(PlaylistForm,self).__init__(*args,**kwargs)
        self.fields['songs'].widget.attrs.update({'class':'form-control'})
        self.fields['name'].widget.attrs.update({'class':'form-control'})


class RecommendationForm(forms.ModelForm):
    score = forms.IntegerField(label="Punteggio", min_value=1, max_value=5)
    song = forms.ModelChoiceField(
        label="Canzone",
        queryset=Song.objects.all()
    )

    class Meta:
        model = Recommendations
        fields = ['score', 'song']

    def __init__(self, *args, **kwargs):
        super(RecommendationForm, self).__init__(*args, **kwargs)
        self.fields['song'].widget.attrs.update({'class': 'form-control'})
        self.fields['score'].widget.attrs.update({'class': 'form-control'})
