from django.urls import path
from .views import UserList,getOrders,addOrdrs,filterData
urlpatterns = [

    path('userlist/',UserList , name="userlist"),
    path('getorders/',getOrders , name="getorders"),
    path('addorders/',addOrdrs , name="addorders"),
    path('filterData/<fromdate>/<todate>',filterData , name="filterData"),
]
