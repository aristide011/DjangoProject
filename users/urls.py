from django .urls import path
from .views import (UserRegisterView, CustomUserUpdateView, CustomUserDeleteView, UserProfileDeleteView,
                     UserProfileUpdateView,
                    UserProfileView,UserAdminUpdateView,UserLoginView,UserLogoutView,UserListView,home_view)

app_name="users"

urlpatterns=[
    path('register/',UserRegisterView.as_view(),name='register'),
    path ('update/<int:pk>/',CustomUserUpdateView.as_view(),name='custom_update'),
    path('admin/update/<int:pk>/',UserAdminUpdateView.as_view(),name='admin_profile_update'),
    path('delete/<int:pk>',CustomUserDeleteView.as_view(),name='customUser_confirm_delete'),
    path('profile/',UserProfileView.as_view(),name='profile'),
    path('profile/update',UserProfileUpdateView.as_view(),name='profile_update'),
    path('profile/<pk>/delete',UserProfileDeleteView.as_view(),name='userProfile_confirm_delete'),
    #URL per il login e logout dell'utente
    path('login/',UserLoginView.as_view(), name='user_login'),
    path('logout/',UserLogoutView.as_view(),name='user_logout'),

    path('list/', UserListView.as_view(), name='user_list'),

    path('', home_view, name='home'),







]