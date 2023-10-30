from django.contrib import admin
from .models import user
# Register your models here.
class Adminuser(admin.ModelAdmin):
    list_display=('UserID','EmailID','Role','UserStatus')

admin.site.register(user,Adminuser)