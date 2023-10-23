from django.shortcuts import render
import json
from django.http import JsonResponse
from JoDate.database import *
from JoDate.menu import *
from apscheduler.schedulers.background import BackgroundScheduler
import time

# Create your views here.

def home(request):
    return render(request,"base.html")

# 登入驗證
def login(request):
    if request.method == "POST":
        json_dict = json.loads(request.body.decode('utf-8'))
        result = loginUser(json_dict)
        return JsonResponse(result)
    return JsonResponse({'Error': 'The resource was not found'}, status=404)

# 註冊
def register(request):
    if request.method == "POST":
        json_dict = json.loads(request.body.decode('utf-8'))
        result = createUser(json_dict)
        return JsonResponse(result)
    return JsonResponse({'Error': 'The resource was not found'}, status=404)

# 更新使用者
def modifyUser(request):
    if request.method == "POST":
        json_dict = json.loads(request.body.decode('utf-8'))
        result = updateUser(json_dict)
        return JsonResponse(result)
    return JsonResponse({'Error': 'The resource was not found'}, status=404)

# 更新使用者密碼
def changePassword(request):
    if request.method == "POST":
        json_dict = json.loads(request.body.decode('utf-8'))
        result = updatePassword(json_dict)
        return JsonResponse(result)
    return JsonResponse({'Error': 'The resource was not found'}, status=404)

# 刪除使用者
def removeUser(request):
    if request.method == "POST":
        json_dict = json.loads(request.body.decode('utf-8'))
        result = deleteUser(json_dict)
        return JsonResponse(result)
    return JsonResponse({'Error': 'The resource was not found'}, status=404)

# 更新使用者
def getUserInfo(request):
    if request.method == "POST":
        json_dict = json.loads(request.body.decode('utf-8'))
        result = getUser(json_dict)
        return JsonResponse(result)
    return JsonResponse({'Error': 'The resource was not found'}, status=404)

# 顯示使用者的所有群組
def getUserGroups(request):
    if request.method == "POST":
        json_dict = json.loads(request.body.decode('utf-8'))
        result = getAllUserGroups(json_dict)
        return JsonResponse(result)
    return JsonResponse({'Error': 'The resource was not found'}, status=404)

# 建立群組
def grouping(request):
    if request.method == "POST":
        json_dict = json.loads(request.body.decode('utf-8'))
        result = createGroup(json_dict)
        return JsonResponse(result)
    return JsonResponse({'Error': 'The resource was not found'}, status=404)

# 更新群組
def modifyGroup(request):
    if request.method == "POST":
        json_dict = json.loads(request.body.decode('utf-8'))
        result = updateGroup(json_dict)
        return JsonResponse(result)
    return JsonResponse({'Error': 'The resource was not found'}, status=404)

# 更新群組的人數
def modifyAttendance(request):
    if request.method == "POST":
        json_dict = json.loads(request.body.decode('utf-8'))
        result = updateAttendance(json_dict)
        return JsonResponse(result)
    return JsonResponse({'Error': 'The resource was not found'}, status=404)

# 顯示單一群組
def getGroupInfo(request):
    if request.method == "POST":
        json_dict = json.loads(request.body.decode('utf-8'))
        result = getGroupbyID(json_dict)
        return JsonResponse(result)
    return JsonResponse({'Error': 'The resource was not found'}, status=404)

# 顯示所有群組
def getAllGroups(request):
    if request.method == "POST":
        json_dict = json.loads(request.body.decode('utf-8'))
        result = getGroups(json_dict)
        return JsonResponse(result)
    return JsonResponse({'Error': 'The resource was not found'}, status=404)

# 特定使用者是否在群組內
def checkAttendance(request):
    if request.method == "POST":
        json_dict = json.loads(request.body.decode('utf-8'))
        result = getAttendanceStatus(json_dict)
        return JsonResponse(result)
    return JsonResponse({'Error': 'The resource was not found'}, status=404)

# 檢查組團是否過期
def checkGroupStatus(request):
    if request.method == "POST":
        result = updateGroupStatus()
        # If safe is True and a non-dict object is passed as the first argument, a TypeError will be raised
        return JsonResponse(result, safe=False)
    return JsonResponse({'Error': 'The resource was not found'}, status=404)

# 定期更新組團狀態
def autoUpdateGroupStatus():
    print('auto updating ',time.strftime('%Y-%m-%d %H:%M:%S'))
    try:
        # UTC+8 = Taipei時間
        TW_now = timezone.now() + timedelta(hours=8)
        groups = Group.objects.filter(status__in = ['FU', 'A'])
        for group in groups:
            #  統一比較時間格式(UTC+8)
            if group.date<TW_now:
                if group.actual>=group.min_require:
                    # 有成團
                    group.status = "C"
                else:
                    # 未成團
                    group.status = "FA"
                    # 信望值下降
                    creator = Users.objects.get(uid=group.creator)
                    creator.credit-=1
                    creator.save() 
                group.save()
    except DatabaseError as e:
        print(str(e))
    except Exception as e:
        print('Invalid data format')

try:
    scheduler = BackgroundScheduler()
    # 每隔一分鐘 自動更新一次
    scheduler.add_job(autoUpdateGroupStatus,'interval',minutes=1,id="updatejob")
    scheduler.start()
    print('scheduler init success ',time.strftime('%Y-%m-%d %H:%M:%S'))
except Exception as e:
    print('error ', str(e))


