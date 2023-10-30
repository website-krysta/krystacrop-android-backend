from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


import datetime
# Create your views here.
from .models import user
from .serializers import UserSerializer

current_date = datetime.datetime.now().date()
current_date_time = datetime.datetime.now()

@api_view(['GET'])
def UserList(request):
    if request.method == 'GET':
        queryset = user.objects.filter(UserStatus=True)
        serializer_data = UserSerializer(queryset ,many=True)
        return Response(serializer_data.data)
    
# @api_view(['POST'])
# def addmaterial(request):
#     if request.method == 'POST':
#         meterial_data = meterialSerializer(data = request.data)
#         if meterial_data.is_valid():
#             meterial_data.save()
#             return Response(meterial_data.initial_data, status=status.HTTP_201_CREATED)
#         return Response(meterial_data.errors, status=status.HTTP_400_BAD_REQUEST)