from django.urls import path
from . import views

urlpatterns = [
   path('', views.home),
    path('user/signup',views.register),
    path('user/signin',views.login),
    path('user/password',views.changePassword),
    path('user/update',views.modifyUser),
    path('user/delete',views.removeUser),
    path('user/get',views.getUserInfo),
    path('user/groups',views.getUserGroups),
    path('group/create',views.grouping),
    path('group/update/info',views.modifyGroup),
    path('group/update/status',views.checkGroupStatus),
    # 新增或移除參與者
    path('group/update/attendance',views.modifyAttendance),
    path('group/get',views.getGroupInfo),
    path('group/all',views.getAllGroups),
    path('user/groups/attended',views.checkAttendance),
]