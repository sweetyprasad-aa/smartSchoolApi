from django.contrib import admin
from accounts.models import UserDetails

# Register your models here.

class UserBasicDetailsAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'date_of_birth')
admin.site.register( UserDetails, UserBasicDetailsAdmin)
