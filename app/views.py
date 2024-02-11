import csv
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render,redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib import messages
from django.http import JsonResponse, HttpResponseBadRequest
# import datetime
from datetime import datetime, time
from django.contrib.auth import logout
# Create your views here.
from django.utils import timezone
from .models import user,orders
from .serializers import UserSerializer,OrdersSerializer
from django.db.models import Q
from dateutil import parser as date_parser
from django.utils.dateparse import parse_datetime

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


# def Orders(request):
#     Orders = orders.objects.all().order_by('-OrdersId')
#     return render(request, 'uifiles/orders.html',{"Orderslist":Orders})
# def Orders(request):
#     if request.method == "POST":
#         fromDate=request.POST.get('fromDate')
#         toDate=request.POST.get('toDate')
#         searchresult = orders.objects.raw('select DealerName,ProductName,ProductQuantity,TransporterName,DateStr from orders where DateStr between "'+fromDate+'" and "'+toDate+'"')
#         return render(request, 'uifiles/orders.html',{"Orderslist":searchresult})
#     else:
#         Orders = orders.objects.all().order_by('-OrdersId')
#         return render(request, 'uifiles/orders.html',{"Orderslist":Orders})
# def Orders(request):
#     if request.method == "POST":
#         fromDate = request.POST.get('fromDate')
#         toDate = request.POST.get('toDate')
#         print(fromDate,toDate)
#         x = toDate
      
#         from_date = datetime.strptime(fromDate, '%Y-%m-%d')
#         to_Date = datetime.strptime(toDate, '%Y-%m-%d')
#         formatted_f_date = from_date.strftime('%d-%m-%Y')
#         formatted_t_date = to_Date.strftime('%d-%m-%Y')
      
#         print(formatted_f_date,formatted_t_date)

        
#         search_result = orders.objects.filter(DateStr__range=[formatted_f_date,formatted_t_date]).order_by('-OrdersId')

#         return render(request, 'uifiles/orders.html', {"Orderslist": search_result,"fromDate": fromDate, "toDate": toDate})
#     else:
#         Orderslist = orders.objects.all().order_by('-OrdersId')
#         return render(request, 'uifiles/orders.html', {"Orderslist": Orderslist})


def Orders(request):
    if request.method == "POST":
        fromDate = request.POST.get('fromDate')
        toDate = request.POST.get('toDate')
        print(fromDate, toDate)

        
        from_date = datetime.strptime(fromDate, '%Y-%m-%dT%H:%M')
        to_date = datetime.strptime(toDate, '%Y-%m-%dT%H:%M')
        formatted_f_date_str = from_date.strftime('%d-%m-%Y')
        formatted_f_time_str = from_date.strftime('%H:%M')
        formatted_t_date_str = to_date.strftime('%d-%m-%Y')
        formatted_t_time_str = to_date.strftime('%H:%M')

        print(formatted_f_date_str, formatted_f_time_str)
        print(formatted_t_date_str, formatted_t_time_str)

        
        all_orders = orders.objects.all().order_by('-OrdersId')
        search_result = [
            order for order in all_orders
            if (formatted_f_date_str < order.DateStr or
                (formatted_f_date_str == order.DateStr and formatted_f_time_str <= order.TimeStr)) and
               (order.DateStr < formatted_t_date_str or
                (order.DateStr == formatted_t_date_str and order.TimeStr <= formatted_t_time_str))
        ]
        f_month_str = from_date.strftime('%m')
        t_month_str = to_date.strftime('%m')
        
        final = [
            item for item in search_result
            if 
        (f_month_str == item.DateStr[3:5] or t_month_str == item.DateStr[3:5] ) and
       
        (item.DateStr[3:5] == t_month_str or f_month_str == item.DateStr[3:5])
]
    
        

        return render(request, 'uifiles/orders.html', {"Orderslist": final, "fromDate": fromDate, "toDate": toDate})
    else:
        Orderslist = orders.objects.all().order_by('-OrdersId')
        return render(request, 'uifiles/orders.html', {"Orderslist": Orderslist})    
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
# @api_view(['GET'])
# def filterData(request,fromdate,todate):
#     if request.method == 'GET':
#         fDate = fromdate
#         tDate = todate
#         fDate = datetime.strptime(fromdate, '%Y-%m-%dT%H:%M')
#         tDate = datetime.strptime(todate, '%Y-%m-%dT%H:%M')
#         print(fDate,tDate)
       
#         orders_data = orders.objects.all()
#         resultData = []
#         for item in orders_data:
#             day = item.DateStr[0:2]
#             month =item.DateStr[3:5]
#             year = item.DateStr[6:10]
#             print(item.TimeStr)
#             formatted_date = f'{year}-{month}-{day}'

          
#             iDate =  datetime.strptime(formatted_date, '%Y-%m-%d')
#             if fDate <= iDate <= tDate:
#                 resultData.append(item)
#         response = HttpResponse(content_type='text/csv')
#         response['Content-Disposition'] = 'attachment; filename="orders_data.csv"'

#         writer = csv.writer(response)
#         writer.writerow(['Dealer Name', 'Product Name', 'Cases', 'Transport Name', 'Address', 'Date', 'Time'])

#         for order in resultData:
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

# from dateutil import parser




@api_view(['GET'])
def filterData(request, fromdate, todate):
    if request.method == 'GET':
        fDate = datetime.strptime(fromdate, '%Y-%m-%dT%H:%M')
        tDate = datetime.strptime(todate, '%Y-%m-%dT%H:%M')
        
        
        start_day = f'{fDate.day:02}'
        start_month = f'{fDate.month:02}'
        
        end_day = f'{tDate.day:02}'
        end_month = f'{tDate.month:02}'
        
        
        start_date = f"{start_day}-{start_month}-{fDate.year}"
        end_date = f"{end_day}-{end_month}-{tDate.year}"

        # f_date_str = fDate.strftime('%d-%m-%Y')
        # f_time_str = fDate.strftime('%H:%M')
        # t_date_str = tDate.strftime('%d-%m-%Y')
        # t_time_str = tDate.strftime('%H:%M')
        
        # print(f_date_str, f_time_str)
        # print(t_date_str, t_time_str)

        all_orders = orders.objects.filter(Q(DateStr__icontains=str(start_date)) | Q(DateStr__icontains=str(end_date))).order_by('-OrdersId')
        final = all_orders
        # f_month_str = fDate.strftime('%m')
        # t_month_str = tDate.strftime('%m')
        
#         final = [
#             item for item in search_result
#             if 
#         (f_month_str == item.DateStr[3:5] or t_month_str == item.DateStr[3:5]  ) and
       
#         (item.DateStr[3:5] == t_month_str or f_month_str == item.DateStr[3:5] )
# ]
        

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="orders_data.csv"'
        

        writer = csv.writer(response)
        writer.writerow(['Dealer Name', 'Product Name', 'Cases', 'Transport Name', 'Address', 'Date', 'Time'])
        # print(final)
        for order in final:
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
   
