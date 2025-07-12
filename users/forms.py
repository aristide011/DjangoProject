from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth import get_user_model

from users.models import CustomUser


class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model=get_user_model()
        fields=['email','first_name','last_name','favorite_genres','birthdate']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Le password non corrispondono.")
        return password2

class UserLoginForm(LoginView):
    template_name='users/login.html'
    form_class=AuthenticationForm

    def get_success_url(self):
        return reverse('music_streaming:song_list')

    def form_valid(self, form):
        # Log the user in
        login(self.request, form.get_user())
        return super().form_valid(form)


