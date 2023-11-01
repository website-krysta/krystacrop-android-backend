from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render,redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib import messages
from django.http import JsonResponse, HttpResponseBadRequest
import datetime
from django.contrib.auth import logout
# Create your views here.
from .models import user,orders
from .serializers import UserSerializer,OrdersSerializer

current_date = datetime.datetime.now().date()
current_date_time = datetime.datetime.now()

def Login(request):
    if request.method == "POST":
        email = request.POST.get('email',"")
        password = request.POST.get('password',"")
        User = user.objects.all()
        for myuser in User:
            if myuser.EmailID == email and myuser.Password == password:
                return JsonResponse({'message': 'Login successful'})
                # return redirect('/myorders/') 
                # return HttpResponseRedirect('/myorders/')
            else:
            # Authentication failed
                return HttpResponseBadRequest('Invalid username or password')
        
        messages.error(request, 'Invalid username or password')
    return render(request, 'uifiles/login.html')

def Orders(request):
    Orders = orders.objects.all()
    return render(request, 'uifiles/orders.html',{"Orderslist":Orders})



def logout_view(request):
    logout(request)
    return redirect('/') 

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