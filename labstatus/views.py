from django.shortcuts import render, redirect
from datetime import datetime
from django.http import HttpResponse
from django.utils import timezone
from .models import LabMember

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import LabMember
from datetime import datetime
import json

# from .forms import FormClass

@csrf_exempt
def record_entry_exit(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_name = data.get('name')
        inout = data.get('inout')
        time_str = data.get('time')

        try:
            time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return JsonResponse({'status': 'error', 'message': '不正な時間形式です。'}, status=400)

        member, created = LabMember.objects.get_or_create(name=user_name)

        # 在室状況を更新
        member.is_present = (inout == 'in')
        member.last_active = time

        if inout == 'in':
            member.handle_entry(time)
        else:
            member.handle_exit(time)

        member.save()

        return JsonResponse({'status': 'success', 'message': '入退室情報を記録しました。'})
    
    return JsonResponse({'status': 'error', 'message': 'POSTリクエストが必要です。'}, status=405)

def index(request):
    members = LabMember.objects.all().order_by('-is_present', '-last_active')
 
    #htmlのformから名前を受け取る
    input=''
    year = 0
    month = 0

    if request.method == 'POST':
        input = request.POST['input']
        year = request.POST['year_search']
        month = request.POST['month_search']
    
    # 名前が一致した場合memberに代入
    member_record=''
    for mem in members:
        if (input == mem.name):
            member_record = LabMember.objects.get(name=input)
            
    print(type(year))
    stats=''
    if member_record and year and month:
                stats = member_record.get_monthly_stats(year, month)
    # print(stats)
    
    # 指定月の総滞在時間
    total=0
    # 指定月の総滞在日数
    entry=0
    # 指定月の平均滞在時間
    ave_time=0
   
    if stats:
        total=stats.total_time
        print(type(total))
        entry = stats.entry_count
        ave_time = stats.average_daily_time
        
        total = int(total/60)
        # total = int(total)
        total = str(total) +"h"
        ave_time = int(ave_time/60)
        # ave_time = int(ave_time)
        ave_time = str(ave_time) + "h"
    else:
        total='記録がありません'
        entry='記録がありません'
        ave_time='記録がありません'
    
    context = {'members': members, 
               'input': input,
               'year' : year,
               'month': month,
               'member_record' :member_record,
               'total_time' : total,
               'entry' : entry,
               'ave_time' : ave_time }
    
    return render(request, 'index.html', context)

