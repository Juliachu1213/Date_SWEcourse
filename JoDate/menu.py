from JoDate.models import Users,Group
from django.db import DatabaseError
from django.core.exceptions import ObjectDoesNotExist
'''
    取得各種資訊的 read function
'''
# 取得個別使用者
def getUser(info):
    try:
        uid = info.get('uid', None)
        if uid:
            userInfo = Users.objects.filter(uid=uid).values()
            # 沒找到匹配的uid
            assert userInfo
        else:
            return {'Error':'Invalid ID input'}
        result = {'user': list(userInfo)}
        return result
    except AssertionError:
        return {'Error':'uid does not exist'}
    except DatabaseError as e:
        return {'Error':str(e)}
    except Exception as e:
        return {'Error':str(e)}
    
# 取得個別群組
def getGroupbyID(info):
    try:
        gid = info.get('gid', None)
        if gid:
            groupInfo = Group.objects.filter(id=gid).values()
            groupObject = Group.objects.get(id=gid)
            groupRelationships = groupObject.User.all()
            groupAttendance=list()
            for user in groupRelationships:
                # user是ManyToMany關聯的一個對象
                # 格式: "111000006 王小明"
                groupAttendance.append(user.uid+' '+user.name)
            # 沒找到匹配的group
            assert groupInfo
        else:
            return {'Error':'Invalid ID input'}
        # 回傳群組資訊和參與者
        result = {'Group': list(groupInfo),'Group Attendance':groupAttendance}
        return result
    except AssertionError:
        return {'Error':'group ID does not exist'}
    except DatabaseError as e:
        return {'Error':str(e)}
    except Exception as e:
        return {'Error':str(e)}

# 取得所有群組
def getGroups(info):
    try:
        group_type = info.get('type', None)
        if group_type and group_type != "ALL":
            groups = Group.objects.filter(status__in = ['FU', 'A'], type=group_type).values()
        else:
            groups = Group.objects.filter(status__in = ['FU', 'A']).values()
        result = {'groups': list(groups)}
        return result
    except DatabaseError as e:
        return {'Error':str(e)}
    except Exception as e:
        return {'Error':'Invalid data format'}

def getAllUserGroups(info):
    try:
        # 要查詢的成員
        uid=info["uid"]
        groups = Group.objects.filter(User__uid = uid)
        if groups.count() == 0:
            return {'Error':'This user did not join any groups'}
        else:
            result = {'groups': list(groups.values())}
            return result
    except DatabaseError as e:
        return {'Error':str(e)}
    except Exception as e:
        return {'Error':'Invalid data format'}
    
# 特定使用者是否在群組內 
def getAttendanceStatus(info):
    try:
        # 要查詢的成員
        uid=info["uid"]
        # 讀取揪團資訊
        gid=info["group_id"]
        group = Group.objects.get(id=gid)
        newUser = Users.objects.get(uid=uid)
        # 是否為創辦者
        if group.creator==uid:
            return {
                "attended":True,
                "isCreator":True
                }             
        # 確認使用者是否已存在於團內
        for userObj in group.User.all():
            if newUser==userObj:              
                return {
                    "attended":True,
                    "isCreator":False
                    }
            else:
                return {
                    "attended":False,
                    "isCreator":False
                    }             
    except ObjectDoesNotExist:
        return {'Error':'Invalid Group or User ID'}
    except DatabaseError as e:
        return {'Error':str(e)}
    except Exception as e:
        return {'Error':'Invalid data format or time format'}

