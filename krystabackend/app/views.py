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

@api_view(['POST'])
def UserList(request):
    if request.method == 'POST':
        queryset = user.objects.all().values()
        useriem = user.objects.get(EmailID=request.data['EmailID'])
        user_details = {  
                'UserID':0,	
                'EmailID' :'',	
                'Password'  :'',	
                'Role':'',	
                'UserStatus':'',		
        }
        user_details['UserID'] = useriem.UserID
        user_details['EmailID'] = useriem.EmailID
        user_details['Password'] = useriem.Password
        user_details['Role'] = useriem.Role
        user_details['UserStatus'] = useriem.UserStatus

        # userdata = UserSerializer(data = user_details)
        serializer_data = UserSerializer(instance=useriem ,data = user_details)
        if serializer_data.is_valid():
            for fields in queryset:
                if fields['EmailID'] ==  request.data['EmailID']and fields['Password'] == request.data['Password']:
                        return Response(serializer_data.data, status=status.HTTP_200_OK)
# @api_view(['POST'])
# def addmaterial(request):
#     if request.method == 'POST':
#         meterial_data = meterialSerializer(data = request.data)
#         if meterial_data.is_valid():
#             meterial_data.save()
#             return Response(meterial_data.initial_data, status=status.HTTP_201_CREATED)
#         return Response(meterial_data.errors, status=status.HTTP_400_BAD_REQUEST)