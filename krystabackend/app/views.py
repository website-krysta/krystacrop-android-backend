import csv
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render,redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib import messages
from django.http import JsonResponse, HttpResponseBadRequest
# import datetime
from datetime import datetime
from django.contrib.auth import logout
# Create your views here.
from django.utils import timezone
from .models import user,orders
from .serializers import UserSerializer,OrdersSerializer

current_date = datetime.now().date()
current_date_time = datetime.now()

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

# def index(request):
#     return render(request, 'uifiles/index.html')


def Orders(request):
    Orders = orders.objects.all().order_by('-OrdersId')
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
        queryset = orders.objects.order_by('-OrdersId')
        # queryset = orders.objects.order_by('OrdersId')
        # RawMaterial.objects.all().order_by('-MaterialID')
        
        serializer_data = OrdersSerializer(queryset ,many=True)
        return Response(serializer_data.data)

@api_view(['POST']) 
def addOrdrs(request):
    if request.method == 'POST':
        orders_data = OrdersSerializer(data=request.data.get('orderslist', []), many=True)
        if orders_data.is_valid():
            orders_data.save()
            return Response({'StatusCode' : 200,'Message' :'Orders added successfully'}, status=status.HTTP_200_OK)
        return Response({'StatusCode' :400,'Message' :'Something went wrong, please try again'}, status=status.HTTP_400_BAD_REQUEST)


#filter and download filter data ############################
@api_view(['GET'])
def filterData(request,fromdate,todate):
    if request.method == 'GET':
        fDate = fromdate
        tDate = todate
        fDate = datetime.strptime(fromdate, '%Y-%m-%d')
        tDate = datetime.strptime(todate, '%Y-%m-%d')
        # fDate = timezone.make_aware(datetime.strptime(fromdate, '%Y-%m-%d'))
        # tDate = timezone.make_aware(datetime.strptime(todate, '%Y-%m-%d'))
        '10-11-2023'
        orders_data = orders.objects.all()
        resultData = []
        for item in orders_data:
            day = item.DateStr[0:2]
            month =item.DateStr[3:5]
            year = item.DateStr[6:10]
            formatted_date = f'{year}-{month}-{day}'
          
            iDate =  datetime.strptime(formatted_date, '%Y-%m-%d')
            if fDate <= iDate <= tDate:
                resultData.append(item)
            # fday = fromdate[8:10]
            # fmonth = fromdate[5:7]
            # fyear = fromdate[0:4]
             
            # tfday = todate[8:10]
            # tfmonth = todate[5:7]
            # tfyear = todate[0:4]
            # if (day >= fday and month >= fmonth and year>= fyear )

        # orders_data = orders.objects.filter(datetime.strptime(DateStr, '%d-%m-%Y').date()=fDate)
        # orders_data = orders.objects.filter(DateStr__range=[fromdate, todate])
        # orders_data = OrdersSerializer(filtered_orders, many=True)
        # Create a CSV response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="orders_data.csv"'

        writer = csv.writer(response)
        writer.writerow(['Dealer Name', 'Product Name', 'Cases', 'Transport Name', 'Address', 'Date', 'Time'])

        for order in resultData:
            writer.writerow([
                order.DealerName,
                order.ProductName,
                order.ProductQuantity,
                order.TransporterName,
                order.Address,
                order.DateStr,
                order.TimeStr
            ])

        return response  
        # return Response(orders_data.data)
        

# @api_view(['POST'])
# def addOrdrs(request):
#     if request.method == 'POST':
#         # orders_data = OrdersSerializer(data = request.data)
#         orders_data = OrdersSerializer(data=request.data.get('orderslist', []), many=True)
#         if orders_data.is_valid():
#             orders_data.save()
#             return Response({"message": "Orders added successfully"}, status=status.HTTP_201_CREATED)
#             # return Response(orders_data.initial_data, status=status.HTTP_201_CREATED)
#         return Response(orders_data.errors, status=status.HTTP_400_BAD_REQUEST)


# from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# import csv


# def filter_and_download(request):
#     if request.method == 'POST':
#         from_date = request.POST.get('fromDate')
#         to_date = request.POST.get('toDate')

#         # Perform date-based filtering on the 'orders' table
#         filtered_orders = orders.objects.filter(DateStr__range=[from_date, to_date])

#         # Prepare filtered data as CSV and return as a downloadable file
#         response = HttpResponse(content_type='text/csv')
#         response['Content-Disposition'] = 'attachment; filename="filtered_orders.csv"'

#         writer = csv.writer(response)
#         writer.writerow(['DealerName', 'ProductName', 'ProductQuantity', 'TransporterName', 'Address', 'DateStr', 'TimeStr'])

#         for order in filtered_orders:
#             writer.writerow([
#                 order.DealerName,
#                 order.ProductName,
#                 order.ProductQuantity,
#                 order.TransporterName,
#                 order.Address,
#                 order.DateStr,
#                 order.TimeStr
#             ])

#         return response
#     return HttpResponse('Invalid Request')
