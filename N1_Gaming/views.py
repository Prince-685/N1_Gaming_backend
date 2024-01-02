from django.shortcuts import render
import datetime as dt
from api import models as model

def Admindashboard(request):
    today=dt.date.today()
    user_instance=model.CustomUser.objects.all()
    user_detail=[]
    for user in user_instance:
      l=[]
      account_instance=model.Account.objects.filter(user=user,date=today)
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
    tsn_instance=model.TSN.objects.all()
    totalplayedpoints=sum([entry.playedpoints for entry in tsn_instance])
    account_instance=model.Account.objects.all()
    totalearnpoints=sum([entry.earn_points for entry in account_instance])
    endpoints=totalplayedpoints-totalearnpoints
    totalprofit=sum([entry.net_profit for entry in account_instance])

    return render(request,'dashboard.html',{'playedpoint':totalplayedpoints,'earnpoint':totalearnpoints,'endpoint':endpoints,'profit':totalprofit,'userdata':user_detail})

def AddUser(request):
    return render(request,'AddUser.html')

def FeedResult(request):
    return render(request,'Result.html')

def Admin_login_page(request):
    return render(request,'adminLogin.html')

def Admin_pass_change_page(request):
    return render(request,'passAdmin.html')

def Update_Credit(request):
    if request.method=='POST':

        username=request.POST.get('data_username')
        credit=request.POST.get('data_credit')
    
    li=[username,credit]
    return render(request,'UpdateCredit.html',{'row':li})

def Set_Bar(request):
    win_pencent_instance=model.Win_Percent.objects.get(pk=1)
    per=win_pencent_instance.percent
    return render(request,'bar.html',{'percent':per})



from datetime import datetime, timedelta
import logging
import random



logger = logging.getLogger(__name__)




def calculate_Result(playedpoint,numbers,totalplaypoints,given_win_p):
    win_amount=[]
    max_win_amount=totalplaypoints*given_win_p/100
    for i in playedpoint:
        wamount= i*90
        win_amount.append(wamount)
    closest_index = min((i for i, value in enumerate(win_amount) if value < max_win_amount), default=None, key=lambda i: max_win_amount - win_amount[i])
    print(closest_index)
    if closest_index==None:
        generated_number = random.choice([str(num).zfill(2) for num in range(100) if num not in numbers])
        earnpoints=0
        return generated_number,earnpoints

    number=numbers[closest_index]
    earnpoints=win_amount[closest_index]
    return number,earnpoints



def Save_result_earnpoint():
    
    win_percent_instance=model.Win_Percent.objects.first()
    given_win_p=win_percent_instance.percent
    time_str = datetime.now().replace(second=0, microsecond=0).time()
    today=dt.date.today()
    gamedate_time_str=datetime.now().replace(second=0, microsecond=0)
    gamedate_time_str=gamedate_time_str.strftime('%d/%m/%Y %I:%M %p')

    gamedate_time = datetime.strptime(gamedate_time_str, '%d/%m/%Y %I:%M %p')
    if model.TSN.objects.filter(gamedate_time=gamedate_time).exists():
        Tsn_instance=model.TSN.objects.get(gamedate_time=gamedate_time)
            #Calculating Result According to winning Percentage
        game_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']
        result_dict = {}
        earnPoints={}

        for game_name in game_names:
            gplay =model.UserGame.objects.filter(tsn_entry=Tsn_instance, game_name=game_name)
            print(gplay)
            if gplay.exists():
                numbers = [entry.number for entry in gplay]
                playedpoint = [entry.Playedpoints for entry in gplay]
                totalplaypoints = sum([entry.Playedpoints for entry in gplay])
                result = calculate_Result(playedpoint, numbers, totalplaypoints, given_win_p)
                result_dict[game_name]=result[0]
                earnPoints[game_name]=result[1]
            else:
                result_dict[game_name] = f"{random.randint(0, 99):02d}"
                earnPoints[game_name]=0

        print(result_dict,earnPoints)
        date_instance, _ = model.DateModel.objects.get_or_create(date=today)
        time_entry = model.TimeEntryModel(
                date=date_instance,
                Time=time_str,
                A=result_dict['A'],
                B=result_dict['B'],
                C=result_dict['C'],
                D=result_dict['D'],
                E=result_dict['E'],
                F=result_dict['F'],
                G=result_dict['G'],
                H=result_dict['H'],
                I=result_dict['I'],
                J=result_dict['J'],
                K=result_dict['K'],
                L=result_dict['L'],
                M=result_dict['M'],
                N=result_dict['N'],
                O=result_dict['O'],
                P=result_dict['P'],
                Q=result_dict['Q'],
                R=result_dict['R'],
                S=result_dict['S'],
                T=result_dict['T'],
            )        
        time_entry.save()
        
        earnpoint_entry = model.Earn_Point(
                date=date_instance,
                time=time_str,
                A=earnPoints['A'],
                B=earnPoints['B'],
                C=earnPoints['C'],
                D=earnPoints['D'],
                E=earnPoints['E'],
                F=earnPoints['F'],
                G=earnPoints['G'],
                H=earnPoints['H'],
                I=earnPoints['I'],
                J=earnPoints['J'],
                K=earnPoints['K'],
                L=earnPoints['L'],
                M=earnPoints['M'],
                N=earnPoints['N'],
                O=earnPoints['O'],
                P=earnPoints['P'],
                Q=earnPoints['Q'],
                R=earnPoints['R'],
                S=earnPoints['S'],
                T=earnPoints['T'],
            )
        earnpoint_entry.save()

    else:
        game_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']
        result_dict = {}
        earnPoints={}
        for game_name in game_names:
            result_dict[game_name] = f"{random.randint(0, 99):02d}"
            earnPoints[game_name]=0

        date_instance, _ = model.DateModel.objects.get_or_create(date=today)
        time_entry = model.TimeEntryModel(
                date=date_instance,
                Time=time_str,
                A=result_dict['A'],
                B=result_dict['B'],
                C=result_dict['C'],
                D=result_dict['D'],
                E=result_dict['E'],
                F=result_dict['F'],
                G=result_dict['G'],
                H=result_dict['H'],
                I=result_dict['I'],
                J=result_dict['J'],
                K=result_dict['K'],
                L=result_dict['L'],
                M=result_dict['M'],
                N=result_dict['N'],
                O=result_dict['O'],
                P=result_dict['P'],
                Q=result_dict['Q'],
                R=result_dict['R'],
                S=result_dict['S'],
                T=result_dict['T'],
            )        
        time_entry.save()
        
        earnpoint_entry = model.Earn_Point(
                date=date_instance,
                time=time_str,
                A=earnPoints['A'],
                B=earnPoints['B'],
                C=earnPoints['C'],
                D=earnPoints['D'],
                E=earnPoints['E'],
                F=earnPoints['F'],
                G=earnPoints['G'],
                H=earnPoints['H'],
                I=earnPoints['I'],
                J=earnPoints['J'],
                K=earnPoints['K'],
                L=earnPoints['L'],
                M=earnPoints['M'],
                N=earnPoints['N'],
                O=earnPoints['O'],
                P=earnPoints['P'],
                Q=earnPoints['Q'],
                R=earnPoints['R'],
                S=earnPoints['S'],
                T=earnPoints['T'],
            )
        earnpoint_entry.save()




def save_Account_details():
    game_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']
    current_time = datetime.now()
    adjusted_time = current_time - timedelta(minutes=2)
    adjusted_time = adjusted_time.replace(second=0, microsecond=0)
    time = adjusted_time.time()
    userlist=model.CustomUser.objects.all()
    target_date=dt.date.today()
    date_time=str(target_date)+" "+str(time)
    print(date_time)
    
    for user in userlist:
        Playedpoints=0
        earnpoint=0
        transaction_instance=model.Transaction.objects.filter(username=user,date=target_date)
        for i in range(len(transaction_instance)):
            Tsn_instance= model.TSN.objects.filter(transaction=transaction_instance[i], gamedate_time=date_time)
            if Tsn_instance.exists():
                for i in Tsn_instance:
                    Playedpoints=Playedpoints+i.playedpoints
                    date_instance=model.DateModel.objects.get(date=target_date)
                    time_instance=model.TimeEntryModel.objects.get(date=date_instance,Time=time)
                    for game_name in game_names:
                        gplay = model.UserGame.objects.filter(tsn_entry=Tsn_instance, game_name=game_name)
                        if gplay.exists():
                            numbers=[]
                            play_point=[]
                            for g in gplay:
                                numbers.append(g.number)
                                play_point.append(g.Playedpoints)
                            # numbers = [entry.number for entry in gplay]
                            # play_point=[entry.Playedpoints for entry in gplay]
                            res=getattr(time_instance, game_name)
                            if res in numbers:
                                res = numbers.index(res)
                                
                                earnpoint=earnpoint +play_point[res]*90
                
        endpoint=Playedpoints - earnpoint
        Profit=Playedpoints*8/100
        netProfit=endpoint-Profit
        user_instance=model.CustomUser.objects.get(username=user)
        Account_instance=model.Account(
            user=user_instance,
            date=target_date,
            time=time,
            play_points=Playedpoints,
            earn_points=earnpoint,
            end_points=endpoint,
            profit=Profit,
            net_profit=netProfit
        )
        Account_instance.save()

save_Account_details()
