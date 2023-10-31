from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


import datetime
# Create your views here.
from .models import user,orders
from .serializers import UserSerializer,OrdersSerializer

current_date = datetime.datetime.now().date()
current_date_time = datetime.datetime.now()

def Login(request):
    return render(request, 'uifiles/login.html')



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



@api_view(['GET'])
def getOrders(request):
    if request.method == 'GET':
        queryset = orders.objects.all()
        serializer_data = OrdersSerializer(queryset ,many=True)
        return Response(serializer_data.data)

@api_view(['POST'])
def addOrdrs(request):
    if request.method == 'POST':
        orders_data = OrdersSerializer(data = request.data)
        if orders_data.is_valid():
            orders_data.save()
            return Response(orders_data.initial_data, status=status.HTTP_201_CREATED)
        return Response(orders_data.errors, status=status.HTTP_400_BAD_REQUEST)