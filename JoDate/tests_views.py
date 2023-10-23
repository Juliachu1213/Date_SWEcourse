from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from JoDate.database import *
from JoDate.menu import *
from JoDate.views import *
from JoDate.urls import *
from JoDate.models import *

class ViewsTestCase(TestCase):

    def setUp(self):
        self.user = Users.objects.create(uid='111753113@g.nccu.edu.tw', name='Kevin',
                                         password='JJ1234567',self_intro='Hello',
                                         gender='F', department='CS',credit='100')
        self.group = Group.objects.create(creator='111753113@g.nccu.edu.tw', title='Group A', type='A', location='NCCU', 
                                     date=timezone.now(), info='Welcome to Group A!', min_require=1, max_require=5, 
                                     actual=1, status='A')
        alice = Users.objects.get(uid='111753113@g.nccu.edu.tw')
        self.group.User.add(alice)
        

    def test_login(self):
        user = Users.objects.get(uid='111753113@g.nccu.edu.tw')
        user.password = create_password('JJ1234567')
        user.save()

        payload = {
            'uid': '111753113@g.nccu.edu.tw',
            'password': 'JJ1234567'
        }
        # Convert the payload to JSON format
        json_payload = json.dumps(payload)

        # Make a POST request to the login URL
        response = self.client.post('/user/signin', data=json_payload, content_type='application/json')
        expected_result =   {"User Info":{
                "user ID":'111753113@g.nccu.edu.tw',
                "user name": 'Kevin',
            }}

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_result)
    
    def test_register(self):
        payload = {
        'uid': '111753129@g.nccu.edu.tw',
        'username':'May',
        'gender':'F',
        'department':'CS',
        'intro':'Hello',
        'password': 'KK1234567',
        }
        json_payload = json.dumps(payload)
        response = self.client.post('/user/signup', data=json_payload, content_type='application/json')

        expected_result =   {"User Info":{
                "user ID":'111753129@g.nccu.edu.tw',
                "user name": 'May',
            }}
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_result)
    
    def test_modify_user(self):
        payload = {'uid': '111753113@g.nccu.edu.tw','username': 'Kevin', 
                   'intro':'Nothing','url':'https://imgur.com/boT6QuE'}    # Change intro
        response = self.client.post('/user/update',payload, content_type='application/json' )

        self.assertEqual(response.status_code, 200)

        # 進一步驗證修改後的結果
        modified_user = Users.objects.get(name='Kevin')
        self.assertEqual(modified_user.self_intro, 'Nothing')

    
    def test_change_password(self):
        user = Users.objects.get(uid='111753113@g.nccu.edu.tw')
        user.password = create_password('JJ1234567')
        user.save()
        payload = {
            "uid": '111753113@g.nccu.edu.tw',
            "origin_password": 'JJ1234567',
            "password":'JJ7654321'
        }
        response = self.client.post('/user/password', payload, content_type='application/json')
        
        self.assertEqual(response.status_code, 200)   

        # 檢查使用者密碼是否更新成功
        updated_user = Users.objects.get(uid='111753113@g.nccu.edu.tw')
        self.assertTrue(compare_password('JJ7654321', updated_user.password))
    
    def test_remove_user(self):
        payload = {
            'uid': self.user.uid
        }
        response = self.client.post('/user/delete', json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        expected_result = {
             "Delete User Info":{
                "user ID":self.user.uid,
            }
        }
        self.assertEqual(response.json(), expected_result)

    def test_get_user_info(self):
        payload = {
            'uid': self.user.uid
        }
        response = self.client.post('/user/get', json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        expected_result =  {"user": [{"uid": "111753113@g.nccu.edu.tw", "name": "Kevin", 
                 "password": "JJ1234567", "gender": "F", 
                 "department": "CS", "credit": 100, 
                 "self_intro": "Hello", "url": ""}]}
   
        self.assertEqual(response.json(), expected_result)

    '''
        Group Tests
    '''

    def test_get_user_groups(self):

        payload = { 'uid': self.user.uid }
        
        response = self.client.post('/user/groups', json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_grouping(self):
        group_data = {
            'uid': '111753113@g.nccu.edu.tw',
            'title': 'Test Group',
            'type': 'A',
            'location': 'Test Location',
            'date':timezone.now() + timedelta(minutes=30),
            'info': 'Test Group Info',
            'min_require': '2',
            'max_require': '5'
        }
        
        # 發送 POST 請求
        response = self.client.post("/group/create",group_data, content_type='application/json')
        
        # 驗證回應
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertEqual(result['Group Info']['creator'],"111753113@g.nccu.edu.tw")
        self.assertEqual(result['Group Info']['title'],"Test Group")
        self.assertEqual(result['Group Info']['info'],"Test Group Info")


    def test_modify_group(self):

        group_data = {
            "uid":  self.user.uid,
            "group_id": self.group.pk,
            "title": 'Group A',
            "type": "A",
            "location": "NCCU", 
            "info": "Welcome everyone",  # Change
            "delete": False
        }
        response = self.client.post('/group/update/info', group_data, content_type='application/json')

        # 確認回傳狀態碼是否為 200 OK
        self.assertEqual(response.status_code, 200)
        
        expected_result = {"Group Info": {"creator": "111753113@g.nccu.edu.tw", "group ID": self.group.pk, "title": "Group A", 
                                          "info": "Welcome everyone",
                                          "location": "NCCU", "type": "A", "status": "A", "min_require": 1, "max_require": 5, "actual": 1}}
        
        self.assertEqual(response.json(),expected_result)

    def test_modify_attendance_add(self):   # 新增
        Users.objects.create(uid='111753129@g.nccu.edu.tw', name='May',
                                         password='KK1234567',self_intro='Hello',
                                         gender='F', department='CS',credit='100')
        group_data = {
            "uid": "111753129@g.nccu.edu.tw",
            "group_id": self.group.pk,
            "operation": "add"
        }
        response = self.client.post('/group/update/attendance', group_data, content_type='application/json')

        # 確認回傳狀態碼是否為 200 OK
        self.assertEqual(response.status_code, 200)
        expected_result = {"Group Info": {"new user ID": "111753129@g.nccu.edu.tw", "group ID": self.group.pk, "status": "A"}}
        self.assertEqual(response.json(),expected_result)

    def test_get_group_info(self):

        group_data = {
            "gid": self.group.pk
        }
        response = self.client.post('/group/get', group_data, content_type='application/json')

        # 確認回傳狀態碼是否為 200 OK
        self.assertEqual(response.status_code, 200)

        # 解析 JSON 回傳結果
        result = json.loads(response.content)

        # 確認結果是否符合預期
        self.assertIn("Group", result)
        self.assertIn("Group Attendance", result)
        expected_attendance = ['111753113@g.nccu.edu.tw Kevin']    
        self.assertEqual(result["Group Attendance"],expected_attendance)   
    
    def test_get_all_groups(self):
        # 模擬 POST 請求，指定特定群組類型
        json_data = {
            "type": "A"
        }
        response = self.client.post('/group/all', json.dumps(json_data), content_type='application/json')

        # 確認回傳狀態碼是否為 200 OK
        self.assertEqual(response.status_code, 200)

        # 解析 JSON 回傳結果
        result = json.loads(response.content)

        # 確認結果是否符合預期
        self.assertIn("groups", result)
        for group in result["groups"]:
            self.assertEqual(group["type"], "A")

    def test_check_attendance(self):
        # 假設存在的群組和成員
        group_id = self.group.pk
        user_id = self.user.uid

        # 模擬 POST 請求
        json_data = {
            "group_id": group_id,
            "uid": user_id
        }
        response = self.client.post('/user/groups/attended', json.dumps(json_data), content_type='application/json')

        # 確認回傳狀態碼是否為 200 OK
        self.assertEqual(response.status_code, 200)

        # 解析 JSON 回傳結果
        result = json.loads(response.content)

        # 確認結果是否符合預期
        self.assertIn("attended", result)
        self.assertIn("isCreator", result)
        self.assertTrue(result["attended"])
        self.assertTrue(result["isCreator"])

def test_check_group_status(self):
        
        response = self.client.post('group/update/status')

        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertIsInstance(result, list)

def test_autoUpdateGroupStatus(self):
        TW_now = timezone.now() + timedelta(hours=8)

        # 調用自動更新群組狀態的函式
        autoUpdateGroupStatus()

        # 檢查群組狀態是否已正確更新
        updated_group = Group.objects.get(id=self.group.id)
        self.assertEqual(updated_group.status, 'C')

        # 檢查使用者信望值是否已正確下降
        updated_user = Users.objects.get(uid=self.user.uid)
        self.assertEqual(updated_user.credit, 9)
      
     
    





    





 

        
