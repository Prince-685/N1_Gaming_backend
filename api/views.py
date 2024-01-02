import datetime as dt
from datetime import datetime, timezone
from django.db import transaction as db_transaction
from django.contrib import messages
import json, re, time, random
import pytz
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser, DateModel, TimeEntryModel, Admin, Transaction, TSN, UserGame,Account,Win_Percent
from .serializers import CustomUserSerializer, TimeEntrySerializer, TransactionSerializer, TSNSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

@csrf_exempt
def user_list(request):
    if request.method == 'GET':
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        # Extract 'is_block' values from the serializer data
        is_blocked_values = [item['is_block'] for item in serializer.data]
        # Create a list 'b' indicating 'blocked' or 'active'
        b = ['blocked' if value else 'active' for value in is_blocked_values]
        row=[[item['username'],item['password'],item['credit'],b[index]] for index,item in enumerate(serializer.data)]
        return render(request,'AddUser.html',{'rows':row})

@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        data = request.POST
        serializer = CustomUserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            users = CustomUser.objects.all()
            serializer = CustomUserSerializer(users, many=True)
            # Extract 'is_block' values from the serializer data
            is_blocked_values = [item['is_block'] for item in serializer.data]
            # Create a list 'b' indicating 'blocked' or 'active'
            b = ['blocked' if value else 'active' for value in is_blocked_values]
            row=[[item['username'],item['password'],item['credit'],b[index]] for index,item in enumerate(serializer.data)]
            messages.success(request, 'User Created Successfully')
            return render(request,'AddUser.html',{'rows':row})
        else:
            messages.error(request, 'An error occurred User not Created')
            return render(request,"AddUser.html")

@csrf_exempt
def user_delete(request, uid):
    try:
        user = CustomUser.objects.get(uid=uid)
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    if request.method == 'GET':
        serializer = CustomUserSerializer(user)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'DELETE':
        user.delete()
        return JsonResponse({'message': 'User deleted successfully'}, status=204)
    

@api_view(['POST'])
@permission_classes([AllowAny])
def save_result(request):
    if request.method == 'POST':
        data = request.POST

         # Extract data from the form
        time = data.get('time')
        A=data.get('A', 0)
        B=data.get('B', 0)
        C=data.get('C', 0)
        D=data.get('D', 0)
        E=data.get('E', 0)
        F=data.get('F', 0)
        G=data.get('G', 0)
        H=data.get('H', 0)
        I=data.get('I', 0)
        J=data.get('J', 0)
        K=data.get('K', 0)
        L=data.get('L', 0)
        M=data.get('M', 0)
        N=data.get('N', 0)
        O=data.get('O', 0)
        P=data.get('P', 0)
        Q=data.get('Q', 0)
        R=data.get('R', 0)
        S=data.get('S', 0)
        T=data.get('T', 0)

        current_datetime = datetime.now()
        

        # Create DateModel instance
        date_instance, _ = DateModel.objects.get_or_create(date=current_datetime.date())

        time_match = re.match(r'(\d{1,2}:\d{2})([ap]m)?', time)
        if time_match:
                time_str = time_match.group(1)
                time_str += ":00"
        existing_data = TimeEntryModel.objects.filter(date=date_instance, Time=time_str).first()

        if existing_data:
            return render(request, 'Result.html', {'new_data': data,'existing_data':existing_data})
        
        else:
           

            # Create TimeEntryModel instance
            time_entry = TimeEntryModel(
                date=date_instance,
                Time=time_str,
                A=A,
                B=B,
                C=C,
                D=D,
                E=E,
                F=F,
                G=G,
                H=H,
                I=I,
                J=J,
                K=K,
                L=L,
                M=M,
                N=N,
                O=O,
                P=P,
                Q=Q,
                R=R,
                S=S,
                T=T,
            )        
            time_entry.save()
            messages.success(request, 'Result Saved Successfully')
            return render(request,'Result.html')
    else:
        messages.error(request, 'An error occurred Data is not Saved')
        return render(request,"Result.html")


@api_view(['POST'])
@permission_classes([AllowAny])
def Override(request):
    if request.method=='POST':
        data=request.POST.get('newData')
        #Converting it in a Dictionary
        data=data[data.index('{')+1:data.rindex('}')]
        data=data.replace("'", "\"").replace("None", "null")
        json_str = '{' + data + '}'

        # Convert the JSON string to a Python dictionary
        data_dict = json.loads(json_str)
        
        # Extract values for keys 'time', 'A', 'B', ..., 'T'
        time = data_dict['time'][0]
        A = data_dict['A'][0]
        B = data_dict['B'][0]
        C= data_dict['C'][0]
        D= data_dict['D'][0]
        E= data_dict['E'][0]
        F= data_dict['F'][0]
        G= data_dict['G'][0]
        H= data_dict['H'][0]
        I= data_dict['I'][0]
        J= data_dict['J'][0]
        K= data_dict['K'][0]
        L= data_dict['L'][0]
        M= data_dict['M'][0]
        N= data_dict['N'][0]
        O= data_dict['O'][0]
        P= data_dict['P'][0]
        Q= data_dict['Q'][0]
        R= data_dict['R'][0]
        S= data_dict['S'][0]
        T= data_dict['T'][0]

        time_match = re.match(r'(\d{1,2}:\d{2})([ap]m)?', time)
        if time_match:
                time_str = time_match.group(1)
                time_str += ":00" 
        
        date=DateModel.objects.get(date=dt.date.today())
        s=TimeEntryModel.objects.get(date=date, Time=time_str)
        s.A=A
        s.B=B
        s.C=C
        s.D=D
        s.E=E
        s.F=F
        s.G=G
        s.H=H
        s.I=I
        s.J=J
        s.K=K
        s.L=L
        s.M=M
        s.N=N
        s.O=O
        s.P=P
        s.Q=Q
        s.R=R
        s.S=S
        s.T=T
        s.save()

        messages.success(request, 'Result Saved Successfully')
        return render(request,'Result.html')

    else:
        messages.error(request, 'An error occurred Data is not Saved')
        return render(request,"Result.html")


@api_view(['GET'])
@permission_classes([AllowAny])
def show_result(request):
    if request.method == 'GET':
        data = request.GET
        date_str = data.get('date')
        
        if type(date_str)==type(None):
            date_str=dt.date.today()
           
        try:
            date = DateModel.objects.get(date=date_str)
            time_entries = TimeEntryModel.objects.filter(date=date)
            serializer = TimeEntrySerializer(time_entries, many=True)
            filtered_data = [{'Time': item['Time'], **{key: item[key] for key in 'ABCDEFGHIJKLMNOPQRST'}} for item in serializer.data]
            result = [[item['Time']] + [item[key] for key in 'ABCDEFGHIJKLMNOPQRST'] for item in filtered_data]
            return render(request,'todayResult.html',{'result':result,'date':date_str})
        except DateModel.DoesNotExist:
            return render(request,'todayResult.html',{'msg':'error result not found'})
    else:
        return Response({'error': 'GET method is required'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
@permission_classes([AllowAny])
def show_result_app(request):
    if request.method == 'GET':
        data = request.GET
        date_str = data.get('date')
        
        if date_str==dt.date.today():
            return redirect('todayResult')
           
        try:
            date = DateModel.objects.get(date=date_str)
            time_entries = TimeEntryModel.objects.filter(date=date)
            serializer = TimeEntrySerializer(time_entries, many=True)
            filtered_data = [{'Time': item['Time'], **{key: item[key] for key in 'ABCDEFGHIJKLMNOPQRST'}} for item in serializer.data]
            result = [[item['Time']] + [item[key] for key in 'ABCDEFGHIJKLMNOPQRST'] for item in filtered_data]
            
            # Return JsonResponse with the result
            return JsonResponse({'result': result, 'date': date_str})
        except DateModel.DoesNotExist:
            # Return JsonResponse with an error message
            return JsonResponse({'error': 'Result not found for the given date'}, status=status.HTTP_404_NOT_FOUND)
    else:
        # Return JsonResponse with an error message for invalid method
        return JsonResponse({'error': 'GET method is required'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)   


@api_view(['GET'])
@permission_classes([AllowAny])
def show_today_result(request):
    if request.method == 'GET':
        
        try:
            date_str=dt.date.today()
            date_instance = DateModel.objects.get(date=date_str)
            dd=date_instance.date
            # Define your time slots
            time_slots = [
                            '09:30:00', '09:45:00','10:00:00', '10:15:00', '10:30:00', '10:45:00',
                            '11:00:00', '11:15:00', '11:30:00', '11:45:00','12:00:00', '12:15:00',
                            '12:30:00', '12:45:00','13:00:00', '13:15:00', '13:30:00', '13:45:00',
                            '14:00:00', '14:15:00', '14:30:00', '14:45:00','15:00:00', '15:15:00',
                            '15:30:00', '15:45:00','16:00:00', '16:15:00', '16:30:00', '16:45:00',
                            '17:00:00', '17:15:00', '17:30:00', '17:45:00','18:00:00', '18:15:00',
                            '18:30:00', '18:45:00','19:00:00', '19:15:00', '19:30:00', '19:45:00',
                            '20:00:00', '20:15:00', '20:30:00', '20:45:00','21:00:00', '21:15:00',
                            '21:30:00', '21:45:00','22:00:00'
                        ]

            # Assuming current_time is a datetime object
            current_time = datetime.now().time()

            # # Convert current_time to datetime.datetime
            # current_datetime = datetime.combine(dd, current_time)
            
             # Find the closest time slot that is less than or equal to the current time
            filtered_time_slots = [time_slot for time_slot in time_slots if datetime.strptime(time_slot, '%H:%M:%S').time() <= current_time]
            
            # Retrieve entries for the date and closest_time
            time_entries = TimeEntryModel.objects.filter(date=date_instance, Time__in=filtered_time_slots)

            serializer = TimeEntrySerializer(time_entries, many=True)
           
            filtered_data = [{'Time': item['Time'], **{key: item[key] for key in 'ABCDEFGHIJKLMNOPQRST'}} for item in serializer.data]
            result = [[item['Time']] + [item[key] for key in 'ABCDEFGHIJKLMNOPQRST'] for item in filtered_data]

            # Return JsonResponse with the result
            return JsonResponse({'result': result})
        except DateModel.DoesNotExist:
            # Return JsonResponse with an error message
            return JsonResponse({'error': 'Result not found for the given date'}, status=status.HTTP_404_NOT_FOUND)
    else:
        # Return JsonResponse with an error message for invalid method
        return JsonResponse({'error': 'GET method is required'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
@permission_classes([AllowAny])
def show_result_on_time(request):
    if request.method == 'GET':
        
        try:
            date_str=dt.date.today()
            date_instance = DateModel.objects.get(date=date_str)
            dd=date_instance.date
            # Define your time slots
            time_slots = [
                            '09:30:00', '09:45:00','10:00:00', '10:15:00', '10:30:00', '10:45:00',
                            '11:00:00', '11:15:00', '11:30:00', '11:45:00','12:00:00', '12:15:00',
                            '12:30:00', '12:45:00','13:00:00', '13:15:00', '13:30:00', '13:45:00',
                            '14:00:00', '14:15:00', '14:30:00', '14:45:00','15:00:00', '15:15:00',
                            '15:30:00', '15:45:00','16:00:00', '16:15:00', '16:30:00', '16:45:00',
                            '17:00:00', '17:15:00', '17:30:00', '17:45:00','18:00:00', '18:15:00',
                            '18:30:00', '18:45:00','19:00:00', '19:15:00', '19:30:00', '19:45:00',
                            '20:00:00', '20:15:00', '20:30:00', '20:45:00','21:00:00', '21:15:00',
                            '21:30:00', '21:45:00','22:00:00'
                        ]

            # Assuming current_time is a datetime object
            current_time = datetime.now().time()

            # Convert current_time to datetime.datetime
            current_datetime = datetime.combine(dd, current_time)
            recently_passed_time = max(
            (time_slot for time_slot in time_slots if current_datetime >= datetime.combine(dd, datetime.strptime(time_slot, "%H:%M:%S").time())),
            default=None
            )
            
            # Retrieve entries for the date and closest_time
            time_entries = TimeEntryModel.objects.filter(date=date_instance, Time=str(recently_passed_time))
            if type(time_entries)==type(None):
                return JsonResponse("Result Coming Soon!!...")
            serializer = TimeEntrySerializer(time_entries, many=True)
            filtered_data = [{'Time': item['Time'], **{key: item[key] for key in 'ABCDEFGHIJKLMNOPQRST'}} for item in serializer.data]
            result = [[item['Time']] + [item[key] for key in 'ABCDEFGHIJKLMNOPQRST'] for item in filtered_data]

            # Return JsonResponse with the result
            return JsonResponse({'result': result})
        except DateModel.DoesNotExist:
            # Return JsonResponse with an error message
            return JsonResponse({'error': 'Result not found for the given date'}, status=status.HTTP_404_NOT_FOUND)
    else:
        # Return JsonResponse with an error message for invalid method
        return JsonResponse({'error': 'GET method is required'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    if request.method == 'POST':
        # Assuming the request data contains 'username' and 'password'
        data = json.loads(request.body)
        print(data)
        username = data.get('username')
        password = data.get('password')
        user_data=CustomUser.objects.get(username=username)
        credit=user_data.credit
        if username and password:
        # Authenticate the user
            try:
                user = CustomUser.objects.get(username=username)
            except CustomUser.DoesNotExist:
                return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        # Check the password manually 
            if user.password == password:
                if not user.is_block:
                    return JsonResponse({'message': 'Login successful','username':username,'credit':credit}, status=status.HTTP_200_OK)
                else:
                    return JsonResponse({'message': "User is Blocked Contact Admin"},status=status.HTTP_401_UNAUTHORIZED)
            else:
    
                return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            
        else:
            return JsonResponse({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        
    else:
        return JsonResponse({'error': 'POST method is required'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@api_view(['POST','GET'])
@permission_classes([AllowAny])
def Admin_login(request):
    if request.method == 'POST':
        data = request.POST
        username = data.get('username')
        password = data.get('password')

        today=dt.date.today()
        user_instance=CustomUser.objects.all()
        user_detail=[]
        for user in user_instance:
            l=[]
            account_instance=Account.objects.filter(user=user,date=today)
            playedpoints=sum([entry.play_points for entry in account_instance])
            earnpoints=sum([entry.earn_points for entry in account_instance])
            endpoint=playedpoints-earnpoints
            profit=playedpoints*8/100
            net_profit=endpoint-profit
            l.append(user.username)
            l.append(playedpoints)
            l.append(earnpoints)
            l.append(endpoint)
            l.append(profit)
            l.append(net_profit)
            user_detail.append(l)


        tsn_instance=TSN.objects.all()
        totalplayedpoints=sum([entry.playedpoints for entry in tsn_instance])
        account_instance=Account.objects.all()
        totalearnpoints=sum([entry.earn_points for entry in account_instance])
        endpoints=totalplayedpoints-totalearnpoints
        totalprofit=sum([entry.net_profit for entry in account_instance])

        if username and password:
        # Authenticate the user
            try:
                user = Admin.objects.get(username=username)
            except Admin.DoesNotExist:
                return render(request,'adminLogin.html',{'msg':'Invalid Credentials'})

        # Check the password manually (not recommended)
            if user.password == password:

                return render(request,"dashboard.html",{'playedpoint':totalplayedpoints,'earnpoint':totalearnpoints,'endpoint':endpoints,'profit':totalprofit,'userdata':user_detail})
            else:
    
                return render(request,'adminLogin.html',{'msg':'Invalid Credentials'})
            
        else:
            return render(request,'adminLogin.html',{'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        
    else:
        return JsonResponse({'error': 'POST method is required'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@api_view(['POST','PUT'])
@permission_classes([AllowAny])
def update_admin_password(request):
    if request.method == 'POST':
        data=request.POST
        current_password = data.get('cPassword')
        new_password = data.get('newPassword')
        confirm_password=data.get('cfPassword')

        user = Admin.objects.get(username='Pushpendra')

        # Check if the current password is correct
        if user.password==current_password:
            # Check if the new password and confirm password match
            if new_password == confirm_password:
                # Update the admin user's password
                user.password=new_password
                user.save()
                messages.success(request, 'Password updated successfully.')
                return redirect('dashboard')
            else:
                messages.error(request, 'New password and confirm password do not match.')
                render(request, 'passAdmin.html')
        else:
            messages.error(request, 'Incorrect current password.')
            render(request, 'passAdmin.html')
    
    return render(request, 'passAdmin.html')

@csrf_exempt
def Block_user(request):
    if request.method=='POST':
        username=request.POST.get('block')

        user = CustomUser.objects.get(username=username)
       
        if user.is_block:
            user.is_block='False'
        else:
            user.is_block='True'
        user.save()

        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        # Extract 'is_block' values from the serializer data
        is_blocked_values = [item['is_block'] for item in serializer.data]
        # Create a list 'b' indicating 'blocked' or 'active'
        b = ['blocked' if value else 'active' for value in is_blocked_values]
        row=[[item['username'],item['password'],item['credit'],b[index]] for index,item in enumerate(serializer.data)]
        return render(request,'AddUser.html',{'rows':row})

def UpdateCredit(request):
    if request.method=='POST':
        username=request.POST.get('username')
        new_credit=request.POST.get('new_credit')

        user = CustomUser.objects.get(username=username)
        user.credit=new_credit
        user.save()

        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)

        is_blocked_values = [item['is_block'] for item in serializer.data]
        b = ['blocked' if value else 'active' for value in is_blocked_values]
        row=[[item['username'],item['password'],item['credit'],b[index]] for index,item in enumerate(serializer.data)]
        return render(request,'AddUser.html',{'rows':row})

def generate_unique_id():
    # Get the current timestamp
    timestamp = str(int(time.time()))

   
    additional_info = 'A102XNT'
    random_value = str(random.randint(0, 9999))
    # Combine timestamp and additional info and random value
    combined_data = additional_info + timestamp + random_value

    

    return combined_data


@api_view(['POST'])
@permission_classes([AllowAny])
def save_transaction(request):
    if request.method == 'POST':
        dataa = json.loads(request.body)
        uname=dataa.get('username')
        # Extract gamedate_time entries
        gamedate_times = dataa.get('gamedate_times', [])
        if not gamedate_times:
            return JsonResponse({'error': 'select Gametime'}, status=status.HTTP_400_BAD_REQUEST)
        transaction_id = dataa.get('transaction_id')
        playedpoints=dataa.get('points')
        slipdatetime_str=dataa.get('slipdate_time')
        user_games_data = dataa.get('GamePlay', [])
        
        date_str=dt.date.today()

        with db_transaction.atomic():
        # Check if the transaction_id already exists
          if Transaction.objects.filter(transaction_id=transaction_id).exists():
            return JsonResponse({'error': 'transaction id already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        
        # Create Transaction instance
        transaction_data = {
            'transaction_id': transaction_id,
            'username': uname,
            'date':date_str
        }

        

        transaction_serializer = TransactionSerializer(data=transaction_data)
        if transaction_serializer.is_valid():
            transaction_serializer.save()

            transaction_instance=Transaction.objects.get(transaction_id=transaction_id)
            # Loop through gamedate_time entries
            for gamedate_time_str in gamedate_times:
                
                # Format the date string to a Python datetime object
                if gamedate_time_str:
                    gamedate_time = datetime.strptime(gamedate_time_str, '%d/%m/%Y %I:%M %p')
                    slipdatetime = datetime.strptime(slipdatetime_str, '%d/%m/%Y %H:%M:%S')
           
                else:
                    Transaction.objects.filter(transaction_id=transaction_id).delete()
                    return Response({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)

                # Create a unique tsn_id for each entry
                t_id = generate_unique_id()
                # Create TSN instance
                tsn_data =TSN( 
                    transaction= transaction_instance,
                    tsn_id=t_id,
                    gamedate_time=gamedate_time,
                    playedpoints=playedpoints,
                    slipdatetime=slipdatetime,
                )
                tsn_data.save()
                
                #updating credit of User
                uObject= CustomUser.objects.get(username=uname)
                ucredit=uObject.credit - int(playedpoints)
                uObject.credit=ucredit
                

                    # Loop through game_name, number, and points entries in UserGame
                    
                for user_game_data in user_games_data:
                    tsn_instance=TSN.objects.get(tsn_id=t_id)
                    usergame_data=UserGame(
                        user = uname,
                        tsn_entry = tsn_instance,
                        game_name=user_game_data[0],
                        number=user_game_data[2:4],
                        Playedpoints=user_game_data[7:],
                    )
                    usergame_data.save()
                    uObject.save()
                
            return JsonResponse({'success': 'Data saved successfully'})
        else:
            return JsonResponse({'error': transaction_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    return JsonResponse({'error': 'Invalid method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
@permission_classes([AllowAny])
def show_transaction(request):
    # Assuming you have a related_name in the Transaction model
    data=request.GET
    uname=data.get('username')
    
    transactions = Transaction.objects.filter(username=uname).order_by('-transaction_id')[:20]
    
    data = []

    for transaction in transactions:
        tsns = TSN.objects.filter(transaction=transaction).order_by('-gamedate_time')[:20]
        tsns_data = TSNSerializer(tsns, many=True).data

        # Extract only the relevant fields from each TSN entry
        extracted_tsns_data = []
        for tsn_data in tsns_data:
            extracted_tsn_data = {
                "tsn_id": tsn_data.get("tsn_id", ""),
                "gamedate_time": tsn_data.get("gamedate_time", ""),
                "playedpoints": tsn_data.get("playedpoints", ""),
                "slipdatetime": tsn_data.get("slipdatetime", ""),
                "cancel": tsn_data.get("cancel", ""),
            }
            extracted_tsns_data.append(extracted_tsn_data)

        transaction_data = {
            "transaction_id": transaction.transaction_id,
            "tsns": extracted_tsns_data,
        }

        data.append(transaction_data)

    return JsonResponse({'transactionList':data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def show_Account_date(request):
    if request.method=='POST':
        data = json.loads(request.body)
        uname=data.get('username')
        
        date1_str = data.get('date1')
        date2_str = data.get('date2')
        user_instance=CustomUser.objects.get(username=uname)
        if date1_str and date2_str:
            try:
                date1 = datetime.strptime(date1_str, '%d-%m-%Y')
                date1 = date1.strftime('%Y-%m-%d')
                date2 = datetime.strptime(date2_str, '%d-%m-%Y')
                date2 = date2.strftime('%Y-%m-%d')
                
                Account_instance=Account.objects.filter(user=user_instance, date__range=[date1, date2])
                sum_playedpoint=0
                sum_earnpoint=0
                sum_profit=0
                sum_netprofit=0
                sum_endpoint=0
                for i in Account_instance:
                    sum_playedpoint+=i.play_points
                    sum_earnpoint+=i.earn_points
                    sum_profit+=i.profit
                    sum_netprofit+=i.net_profit
                    sum_endpoint+=i.end_points
                agent=0
                detail=[sum_playedpoint,sum_earnpoint,sum_endpoint,sum_profit,agent,sum_netprofit]

                return JsonResponse({'data':detail},status=status.HTTP_200_OK)
            except ValueError:
                return JsonResponse({'error': 'Invalid date format'})
        else:
            date_str=dt.date.today()
            Account_instance=Account.objects.filter(user=user_instance,date=date_str)
            sum_playedpoint=0
            sum_earnpoint=0
            sum_profit=0
            sum_netprofit=0
            sum_endpoint=0
            for i in Account_instance:
                sum_playedpoint+=i.play_points
                sum_earnpoint+=i.earn_points
                sum_profit+=i.profit
                sum_netprofit+=i.net_profit
                sum_endpoint+=i.end_points
            agent=0
            detail=[sum_playedpoint,sum_earnpoint,sum_endpoint,sum_profit,agent,sum_netprofit]

            return JsonResponse({'data':detail},status=status.HTTP_200_OK)
        
    
    return JsonResponse({'error': 'Invalid method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_win_per(request):
    if request.method == 'POST':
        data = request.POST
        per = data.get('percent')
        percent_instance = Win_Percent.objects.first()

        if percent_instance:
            percent_instance.percent = per
            percent_instance.save()
        else:
            Win_Percent.objects.create(percent=per)
        return JsonResponse({'percent': per,"message":"Win percentage set Successfully"})
    
    return render(request, 'bar.html')


@api_view(['POST'])
@permission_classes([AllowAny])
def Redeem_slip(request):
    if request.method=='POST':
        data=json.loads(request.body)
        transaction_id=data.get('transaction_id')
        transaction_instance=Transaction.objects.get(transaction_id=transaction_id)
        tsn_instance=TSN.objects.filter(transaction=transaction_instance)
        earnpoint=0
        for i in tsn_instance:
           
            game_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']
            date_time=i.gamedate_time
            datetime_str=date_time.strftime('%Y-%m-%d %I:%M %p')
            
            date_str=(datetime_str[0:10])
            # time_str=date_time.time()
            desired_timezone = pytz.timezone('Asia/Kolkata')
            combined_datetime_with_timezone = date_time.replace(tzinfo=pytz.utc).astimezone(desired_timezone)
            time_str=combined_datetime_with_timezone.time()
           
           
            try:
                date_instance=DateModel.objects.get(date=date_str)

                try:
                    time_instance=TimeEntryModel.objects.get(date=date_instance,Time=time_str)
                    for slot in game_names:
                        gplay=UserGame.objects.filter(tsn_entry=i,game_name=slot)
                        if gplay.exists():
                            numbers = [entry.number for entry in gplay]
                            play_point=[entry.Playedpoints for entry in gplay]
                            result = getattr(time_instance, slot)
                            
                            if result in numbers:
                                res = numbers.index(result)
                                earnpoint=earnpoint+play_point[res]*90
                            

                except TimeEntryModel.DoesNotExist:
                    continue
            except DateModel.DoesNotExist:
                continue       

        return JsonResponse({'win':earnpoint},status=status.HTTP_200_OK)
    return JsonResponse({'error': 'Invalid method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
               


@api_view(['GET'])
@permission_classes([AllowAny])
def Credit(request):
    data=request.GET
    uname=data.get('username')
    user=CustomUser.objects.get(username=uname)
    credit=user.credit
    
    return JsonResponse({'credit':credit},status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def delete_tsn_entry(request,tsn_id):
   
    if request.method == 'POST':
        try:

            tsn_instance=TSN.objects.get(tsn_id=tsn_id)
            tsn_instance.cancel=True
            tsn_instance.save()
            user_game_instance = UserGame.objects.filter(tsn_entry__tsn_id=tsn_id)
            
            for usergame in user_game_instance:
                usergame.delete()

            return JsonResponse({'msg':'Game Cancelled successfully'},status=status.HTTP_200_OK)

        except UserGame.DoesNotExist:
            return JsonResponse({'error': 'Tsn entry not found.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return JsonResponse({'error': 'Invalid request method.'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([AllowAny])
def ReprintSlip(request,tsn_id):
    if request.method == 'POST':

        try:

            tsn_instance=TSN.objects.get(tsn_id=tsn_id)
            user_game_instance = UserGame.objects.filter(tsn_entry__tsn_id=tsn_id)
            l=[]
            for i in user_game_instance:
                slot=i.game_name
                number=i.number
                points=i.Playedpoints
                value=slot +'-'+str(number)+" "+"-"+" "+str(points)
                l.append(value)
            slipdt=str(tsn_instance.slipdatetime).replace('T'," ").replace('Z',"")
            gamedt=str(tsn_instance.gamedate_time).replace('T'," ").replace('Z',"")
            
            data={}
            data['transaction_id']=tsn_instance.transaction.transaction_id
            data['slipdatetime']=slipdt
            data['gamedate_time']=gamedt
            data['Gameplay']=l
            data['playedpoints']=tsn_instance.playedpoints

            return JsonResponse({'data':data},status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    return JsonResponse({'error': 'Invalid request method.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def User_status(request,uname):
    if request.method=='GET':
        try:
            user_instance=CustomUser.objects.get(username=uname)
            user_status=user_instance.is_block
            return JsonResponse({'user_status':user_status},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return JsonResponse({'error': 'Invalid request method.'}, status=status.HTTP_400_BAD_REQUEST)
