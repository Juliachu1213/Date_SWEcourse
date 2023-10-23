from django.db import models
from datetime import timedelta, datetime
from django.utils import timezone
# Create your models here.
class Users(models.Model):
    # student ID
    uid = models.CharField(max_length=255, primary_key=True,default='000000000')
    gender_option = [
        ("F", "Female"),
        ("M", "Male"),
        ("N", "Non-binary"),
    ]
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255,default="00000000")
    gender = models.CharField(max_length=1, choices=gender_option)
    department = models.CharField(max_length=255)
    credit = models.PositiveIntegerField(default=100)
    # Blank values are stored in the DB as an empty string ('')
    self_intro = models.CharField(max_length=255, blank=True)
    url = models.CharField(max_length=255, blank=True)

class Group(models.Model):
    type_option = [
        ("A", "聯誼"),
        ("B", "打球"),
        ("C", "拼車"),
        ("D", "拚外送"),
        ("O", "其他"),
    ]
    status_option = [
        ("FU", "目前額滿"),
        ("A", "尚有餘額"),
        ("C", "已經結束"),
        ("FA", "未成團"),
        ("NA", "已被刪除"),
    ]
    # 活動創辦者
    creator = models.CharField(max_length=255,default='000000000')
    # event name
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=1, choices=type_option)
    location = models.CharField(max_length=255, default="政大正門校碑")
    # default close time : now + 30 minutes
    def now_plus_30(): 
        return timezone.now() + timedelta(minutes=30)
    date = models.DateTimeField(default=now_plus_30)
    info = models.CharField(max_length=255, blank=True)
    # actual 實際人數
    min_require = models.PositiveIntegerField(default=1)
    max_require = models.PositiveIntegerField(default=10)
    actual = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=255, choices=status_option, default="A")
    # many to many relationship
    User = models.ManyToManyField(Users)

