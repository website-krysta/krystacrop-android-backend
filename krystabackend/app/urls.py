from django.urls import path
from .views import UserList,getOrders,addOrdrs
urlpatterns = [

    path('userlist/',UserList , name="userlist"),
    path('getorders/',getOrders , name="getorders"),
    path('addorders/',addOrdrs , name="addorders"),
]
