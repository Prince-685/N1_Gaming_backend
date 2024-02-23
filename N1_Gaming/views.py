from django.shortcuts import render
import datetime as dt
from api import models as model
import numpy as np


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
    account_instance=model.Account.objects.filter(date=today)
    totalplayedpoints=sum([entry.play_points for entry in account_instance])
    totalearnpoints=sum([entry.earn_points for entry in account_instance])
    endpoints=sum([entry.end_points for entry in account_instance])
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




def wining_result(sold_ticket,percent):
    result={}
    game_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']
    random_slot_list=[]
    for i in game_names:
        playedpoint=sold_ticket[i].values()
        numbers=sold_ticket[i].keys()
        max_win=sum(playedpoint)*percent/100
        if max_win>=min(sold_ticket[i].values())*90:
            mul_playedpoint=list(np.array(list(playedpoint)) * 90)
            closest_index = min((i for i, value in enumerate(mul_playedpoint) if value <= max_win), default=None, key=lambda i: max_win - mul_playedpoint[i])
            result[i]=list(numbers)[closest_index]
        else:
            random_slot_list.append(i)
    remaining_sum=0
    for i in random_slot_list:
        remaining_sum+=sum(sold_ticket[i].values())
    print(remaining_sum)
    max_am=remaining_sum*percent/100
    print(random_slot_list)
    win_slot=random.choice(random_slot_list)
    print(win_slot)
    print(max_am)
    for i in random_slot_list:
        numbers=sold_ticket[i].keys()
        if i==win_slot:
            playedpoint=sold_ticket[i].values()
            mul_playedpoint=list(np.array(list(playedpoint)) * 90)
            closest_index = min((i for i, value in enumerate(mul_playedpoint) if value <= max_am), default=None, key=lambda i: max_am - mul_playedpoint[i])
            if closest_index==None:
                generated_number=-1
                while(True):
                    generated_number=random.randint(0, 99)
                    generated_number="{:02d}".format(generated_number)
                    if(generated_number not in numbers):
                        result[i]=generated_number
                        break
            else:
                result[i]=list(numbers)[closest_index]
        else:
            generated_number=-1
            while(True):
                generated_number=random.randint(0, 99)
                generated_number="{:02d}".format(generated_number)
                if(generated_number not in numbers):
                    result[i]=generated_number
                    break
            
    return result

def Save_result_earnpoint():
    
    win_percent_instance=model.Win_Percent.objects.first()
    given_win_p=win_percent_instance.percent
    time_str = datetime.now().replace(second=0, microsecond=0).time()
    today=dt.date.today()
    gamedate_time_str=datetime.now().replace(second=0, microsecond=0)
    gamedate_time_str=gamedate_time_str.strftime('%d/%m/%Y %I:%M %p')

    gamedate_time = datetime.strptime(gamedate_time_str, '%d/%m/%Y %I:%M %p')

    game_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']
    ticket_sold={}
    if model.TSN.objects.filter(gamedate_time=gamedate_time).exists():
        for game_name in game_names:
            n=[]
            p=[]
            tp=[]
            Tsn_instance=model.TSN.objects.filter(gamedate_time=gamedate_time)
            for t in Tsn_instance:

                gplay =model.UserGame.objects.filter(tsn_entry=t, game_name=game_name)
                if gplay.exists():
                    numbers = [entry.number for entry in gplay]
                    playedpoint = [entry.Playedpoints for entry in gplay]
                    totalplaypoints = sum([entry.Playedpoints for entry in gplay])
                    n.append(numbers)
                    p.append(playedpoint)
                    tp.append(totalplaypoints)
            tppoints=sum(tp)
            if n and p and tppoints:
                number=[]
                points=[]
                for i in range(len(n)):
                    for j in range(len(n[i])):
                        if n[i][j] not in number:
                            
                            number.append(n[i][j])
                            points.append(p[i][j])
                        else:
                            a=number.index(n[i][j])
                            points[a]=points[a]+p[i][j]
                ticket_sold[game_name]=dict(zip(number,points))       
        winresult=wining_result(ticket_sold,given_win_p)
        date_instance, _ = model.DateModel.objects.get_or_create(date=today)
        time_entry = model.TimeEntryModel(
                date=date_instance,
                Time=time_str,
                A=winresult['A'],
                B=winresult['B'],
                C=winresult['C'],
                D=winresult['D'],
                E=winresult['E'],
                F=winresult['F'],
                G=winresult['G'],
                H=winresult['H'],
                I=winresult['I'],
                J=winresult['J'],
                K=winresult['K'],
                L=winresult['L'],
                M=winresult['M'],
                N=winresult['N'],
                O=winresult['O'],
                P=winresult['P'],
                Q=winresult['Q'],
                R=winresult['R'],
                S=winresult['S'],
                T=winresult['T'],
            )        
        time_entry.save()
        

    else:
        game_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']
        result_dict = {}
        for game_name in game_names:
            result_dict[game_name] = f"{random.randint(0, 99):02d}"

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





def save_Account_details():
    
    current_time = datetime.now()
    adjusted_time = current_time - timedelta(minutes=2)
    adjusted_time = adjusted_time.replace(second=0, microsecond=0)
    time = adjusted_time.time()
    userlist=model.CustomUser.objects.all()
    target_date=dt.date.today()
    date_time=str(target_date)+" "+str(time)
    
    
    for user in userlist:
        Playedpoints=0
        earnpoint=0
        transaction_instance=model.Transaction.objects.filter(username=user,date=target_date)
        
        date_instance=model.DateModel.objects.get(date=target_date)
        time_instance=model.TimeEntryModel.objects.get(date=date_instance,Time=time)
        for t in range(len(transaction_instance)):
            
            Tsn_instance= model.TSN.objects.filter(transaction=transaction_instance[t], gamedate_time=date_time)
            
            if Tsn_instance.exists():
                for i in Tsn_instance:
                    Playedpoints=Playedpoints+i.playedpoints
                    
                    gplay = model.UserGame.objects.filter(tsn_entry=i)
                    
                    if gplay.exists():
                        for g in gplay:
                            gname=g.game_name
                            res=getattr(time_instance, gname)
                            if res==g.number:
                                earnpoint=earnpoint +g.Playedpoints*90
                
        endpoint=Playedpoints - earnpoint
        Profit=Playedpoints*8/100
        netProfit=endpoint-Profit
        print(Playedpoints,earnpoint,endpoint,Profit,netProfit)
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
