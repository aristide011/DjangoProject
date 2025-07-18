
from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LoginView  # Impostazione della loginView
from django .views.generic import CreateView,UpdateView,DetailView,DeleteView,ListView,TemplateView
from .models import UserProfile,CustomUser
from .forms import UserRegistrationForm
from django.contrib.auth.mixins import LoginRequiredMixin ,UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect,HttpResponseForbidden,HttpResponse



class UserRegisterView(CreateView):
    form_class=UserRegistrationForm
    template_name='users/register.html'
    success_url = reverse_lazy('users:user_login')

    def form_valid(self,form):
        return super(UserRegisterView,self).form_valid(form)
    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

class CustomUserUpdateView(LoginRequiredMixin,UpdateView):
    model=CustomUser
    fields=['email' ,'favorite_genres','birthdate']
    template_name='users/custom_update.html'
    success_url=reverse_lazy('users:profile')
    success_message="Il tuo profilo è stato aggiornato con successo!"





class CustomUserDeleteView(LoginRequiredMixin,DeleteView):
    model=CustomUser
    success_url=reverse_lazy('users:user_login')
    template_name = 'users/customUser_confirm_delete.html'

    def form_valid(self, form):
        self.object = self.get_object()
        if self.object == self.request.user:
            self.object.delete()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponseForbidden()


class UserListView(ListView):
    model =CustomUser
    template_name ='users/user_list.html'
    context_object_name='users'


    def get_queryset(self):
        query=self.request.GET.get('q')
        if query:
            return CustomUser.objects.filter(Q(first_name__icontains=query)|Q(last_name__icontains=query)| Q(email__icontains=query))
        return CustomUser.objects.all()


class UserProfileView( LoginRequiredMixin ,DetailView):#mostra il profilo dell'utente attualmente loggato
    model=UserProfile
    template_name = 'users/profile.html'

    def get_object(self,queryset=None):
        try:
            return self.request.user.userprofile
        except AttributeError:
            # Gestire l'errore se l'utente non ha un profilo utente associato
            return None


class UserProfileUpdateView(LoginRequiredMixin,UpdateView) :
    model=UserProfile
    fields=['bio','profile_picture']
    template_name = 'users/profile_update.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self,queryset=None):
        return self.request.user.userprofile

    def form_valid (self,form ):
        return super().form_valid(form)


class UserProfileDeleteView(LoginRequiredMixin,DeleteView):
    model=UserProfile
    template_name ='users/userProfile_confirm_delete.html'
    success_url=reverse_lazy('users:user_login')


class UserAdminUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CustomUser
    fields = ['first_name','last_name','email', 'favorite_genres', 'birthdate']
    template_name = 'users/admin_profile_update.html'
    success_url=reverse_lazy('users:user_list')

    def test_func(self):
            return self.request.user.is_superuser

    def form_valid(self, form):
            # Puoi aggiungere logica personalizzata qui, se necessario
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)  # Stampa gli errori per diagnosticare il problema
        return super().form_invalid(form)


    # effettuare il login e il logout

class UserLoginView(LoginView):
    template_name='users/login.html'
    redirect_authenticated_user =True

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('music_streaming:song_list')
class UserLogoutView(LoginRequiredMixin,LogoutView):

    next_page=reverse_lazy('users:user_login')

    def dispatch(self,request,*args, **kwargs):
        messages.success(request ,"Sei stato disconesso con successo.")
        return super().dispatch(request,*args, **kwargs)



def home_view(request):
         return render(request, 'home.html')