from JoDate.models import Users,Group
from JoDate.auth import create_password,compare_password,email_validation
from django.db import DatabaseError
from django.core.exceptions import ObjectDoesNotExist
from django.utils.dateparse import parse_datetime
import zoneinfo
from datetime import timedelta
from django.utils import timezone
'''
    針對資料庫操作的 create,update,delete function
'''

# 建立使用者
def createUser(info):
    try:
        # 讀取使用者資訊
        id=info["uid"]
        # 檢查e-mail格式
        assert "@g.nccu.edu.tw" in id
        # email驗證沒過 則無法註冊
        if not email_validation(id):
            return {'Error':'email validation and verification failed'}
        uname=info["username"]
        gender=info["gender"]
        department=info["department"]
        intro=info["intro"]
        password=create_password(info["password"])
        url=""
        # 不同性別頭貼不同
        if gender=="M":
            url="https://imgur.com/ITSlWZA"
        elif gender=="F":
            url="https://imgur.com/boT6QuE"
        else:
            url="https://imgur.com/akdAD8A"         
        user1 = Users.objects.create(
            uid=id,name=uname,password=password,
            gender=gender, department=department, self_intro=intro,url=url
        )
        user1.save()
        return {
            "User Info":{
                "user ID":id,
                "user name":uname,
            }
        }
    except AssertionError:
        return {'Error':'invalid e-mail format'}
    except DatabaseError as e:
        return {'Error':str(e)}
    except Exception as e:
        return {'Error':str(e)}

# 使用者登入驗證
def loginUser(info):
    try:
        # 讀取使用者資訊
        id=info["uid"] 
        input_password=info["password"] 
        user = Users.objects.get(uid=id)
        if compare_password(input_password,user.password):
            return {
                "User Info":{
                    "user ID":id,
                    "user name":user.name
                }
            }
        # 處理密碼錯誤
        else:
            return {'Error':'Password incorrect'}
    except ObjectDoesNotExist:
        return {'Error':'User does not exist'}
    except DatabaseError as e:
        return {'Error':str(e)}
    except Exception as e:
        return {'Error':'Invalid data format'}
    
# 更新使用者資料
def updateUser(info):
    try:
        # 讀取使用者資訊
        id=info["uid"] 
        uname=info["username"]
        intro=info["intro"]
        url=info["url"] 
        user = Users.objects.filter(uid=id).update(name=uname,self_intro=intro,url=url)
        return {
            "User update Info":{
                "user ID":id,
                "user name":uname,
                "intro":intro
            }
        }
    except ObjectDoesNotExist:
        return {'Error':'User does not exist'}
    except DatabaseError as e:
        return {'Error':str(e)}
    except Exception as e:
        return {'Error':'Invalid data format'}
    
# 更新使用者密碼
def updatePassword(info):
    try:
        # 讀取使用者資訊
        id=info["uid"]
        origin_password=info["origin_password"]
        password=create_password(info["password"]) 
        user = Users.objects.get(uid=id)
        if compare_password(origin_password,user.password):
            user.password=password
            user.save()
            return {
                "User Info":{
                    "user ID":id,
                    "user name":user.name
                }
            }
        # 處理密碼錯誤
        else:
            return {'Error':'Password incorrect'}
    except ObjectDoesNotExist:
        return {'Error':'User does not exist'}
    except DatabaseError as e:
        return {'Error':str(e)}
    except Exception as e:
        return {'Error':'Invalid data format'}
    
# 刪除使用者
def deleteUser(info):
    try:
        # 讀取使用者資訊
        id=info["uid"]
        # 確認使用者是否存在
        Users.objects.get(uid=id)
        Users.objects.filter(uid=id).delete()
        return {
            "Delete User Info":{
                "user ID":id,
            }
        }
    except ObjectDoesNotExist:
        return {'Error':'User not found'}
    except DatabaseError as e:
        return {'Error':str(e)}
    except Exception as e:
        return {'Error':'Invalid data format'}
    
def createGroup(info):
    try:
        # 讀取使用者資訊
        id=info["uid"] 
        # 讀取揪團資訊
        title=info["title"]
        type=info["type"]
        location=info["location"]
        date=info["date"]
        group_info=info["info"]
        min_require=int(info["min_require"])
        max_require=int(info["max_require"])
        if min_require>max_require or min_require<0 or max_require<0:
            return {'Error':'Invalid number input'}
        # 轉換時間/時區
        naive = parse_datetime(date)
        naive = naive.replace(tzinfo=zoneinfo.ZoneInfo("GMT"))
        user1 = Users.objects.get(uid=id)
        # 信用低於80 不能組團
        assert user1.credit>=80
        # 建立組團
        group1 = Group.objects.create(
            creator=id,title=title,type=type,location=location,date=naive,info=group_info,
            min_require=min_require,max_require=max_require
        )
        group1.save()
        # 插入relationship
        group1.User.add(user1)
        return {
                    "Group Info":{
                        "group ID":group1.pk,
                        "creator":id,
                        "title":title,
                        "info":group_info
                    }
                }
    except ObjectDoesNotExist:
        return {'Error':'User does not exist'}
    except AssertionError:
        # 信用太低
        return {'Error':'Bad credit score'}
    except DatabaseError as e:
        return {'Error':str(e)}
    except Exception as e:
        return {'Error':'Invalid data format or time format'}

# 更新揪團資訊 
def updateGroup(info):
    try:
        uid=info["uid"]
        # 讀取揪團資訊
        gid=info["group_id"]
        title=info["title"]
        type=info["type"]
        location=info["location"]
        group_info=info["info"]
        # 若為空字串return false
        onDelete=bool(info["delete"])
        group = Group.objects.get(id=gid)
        assert uid==group.creator
        if not onDelete:
            # 變更組團
            group.title=title
            group.type=type
            group.location=location
            group.info=group_info
            final_status=group.status
            group.save()
        else:
            # 刪除組團並不會在資料庫刪除，而是在介面上不再顯示
            group.status="NA"
            final_status="NA"
            group.save()
        return {
                    "Group Info":{
                        "creator":uid,
                        "group ID":gid,
                        "title":title,
                        "info":group_info,
                        "location":location,
                        "type":type,
                        "status":final_status,
                        "min_require": group.min_require,
                        "max_require": group.max_require,
                        "actual": group.actual,
                    }
                }        
    except ObjectDoesNotExist:
        return {'Error':'Group does not exist'}
    except AssertionError:
        # 修改資訊的人並非創辦者
        return {'Error':'Permission Denied'}
    except DatabaseError as e:
        return {'Error':str(e)}
    except Exception as e:
        return {'Error': str(e)}

# 新增/刪除揪團成員     
def updateAttendance(info):
    try:
        # 要新增的成員
        uid=info["uid"]
        # 讀取揪團資訊
        gid=info["group_id"]
        # 判斷指令為新增還是減少成員
        operation=info["operation"]
        group = Group.objects.get(id=gid)
        newUser = Users.objects.get(uid=uid)
        final_status=group.status
        # 驗證人數是否超過上限/低於下限
        if operation=="add":
            # 組團狀態為"尚有餘額"
            assert final_status=="A"
            # 不可重複加入創辦者
            if group.creator==uid:
                return {'Error':'Cannot add creator'}
            # 確認使用者是否已存在於團內 避免同一個人重複加入
            for userObj in group.User.all():
                if newUser==userObj:
                    return {'Error':'Duplicate insert'}
            # 確保沒有超額
            assert group.actual<group.max_require
            # 如果剛好額滿 更新狀態
            if group.actual+1==group.max_require:
                group.status="FU"
                final_status="FU"
            # 新增成員
            group.User.add(newUser)
            group.actual+=1
            group.save()
            return {
                        "Group Info":{
                            "new user ID":uid,
                            "group ID":gid,
                            "status":final_status
                        }
                    } 
        elif operation=="remove":
            # 移除成員
            # 組團狀態為"尚有餘額"或"目前額滿"
            assert final_status=="A" or final_status=="FU"
            # 不可移除創辦者
            if group.creator==uid:
                return {'Error':'Cannot remove creator'}
            assert group.actual>0  
            group.User.remove(newUser)
            group.actual-=1
            # 如果不再額滿 更新狀態
            if(final_status=="FU"):
                group.status="A"
                final_status="A"                
            group.save()
            return {
                        "Group Info":{
                            "remove user ID":uid,
                            "group ID":gid,
                            "status":final_status
                        }
                    }
        else:
            return {'Error':'No Operation'}            
    except ObjectDoesNotExist as e:
        return {'Error':str(e)}
    except AssertionError:
        # 人數超出上限/小於0
        return {'Error':'Out of range of Participants'}
    except DatabaseError as e:
        return {'Error':str(e)}
    except Exception as e:
        return {'Error':'Invalid data format'}
    
def updateGroupStatus():
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
        refresh = Group.objects.filter(status__in = ['FU', 'A'])
        return list(refresh.values())
    except DatabaseError as e:
        return {'Error':str(e)}
    except Exception as e:
        return {'Error':'Invalid data format'}
    