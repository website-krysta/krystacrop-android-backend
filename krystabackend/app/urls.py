from django.urls import path
from .views import UserList
urlpatterns = [
    path('userlist/',UserList , name="userlist"),
]
