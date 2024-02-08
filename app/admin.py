from django.contrib import admin
from .models import user,orders
# Register your models here.
class Adminuser(admin.ModelAdmin):
    list_display=('UserID','EmailID','Role','UserStatus')
class AdminOrders(admin.ModelAdmin):
    list_display=('OrdersId','DealerName','TransporterName','Address','ProductName','ProductQuantity','DateStr')

admin.site.register(user,Adminuser)
admin.site.register(orders,AdminOrders)