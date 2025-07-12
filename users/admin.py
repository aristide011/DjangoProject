from django.contrib import admin
from .models import CustomUser,UserProfile


class CustomUserAdmin (admin.ModelAdmin):
    list_display =('email','first_name','last_name','is_curator')

class UserProfileAdmin(admin.ModelAdmin) :
    list_display=('user','bio')


admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
