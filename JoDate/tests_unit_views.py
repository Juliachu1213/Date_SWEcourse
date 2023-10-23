from django.test import TestCase
from unittest.mock import patch
import json
from django.http import JsonResponse
from JoDate.database import *
from JoDate.menu import *
from JoDate.views import *
from django.test import TestCase, RequestFactory
from django.http import JsonResponse
import datetime
from unittest.mock import Mock

class LoginViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        
    def test_login(self):

        with patch('JoDate.models.Users.objects.get') as mock_get:
        
            mock_user = Users(uid='111753113@g.nccu.edu.tw', password=create_password('password123'), name='John')
            mock_get.return_value = mock_user

            data = {
            'uid': '111753113@g.nccu.edu.tw',
            'password': 'password123'
            }
            request = self.factory.post('/login/', data=json.dumps(data), content_type='application/json')
            response = login(request)
        
            expected_response = {
            "User Info": {
                "user ID": "111753113@g.nccu.edu.tw",
                "user name": "John"
             }
            }

            mock_get.assert_called_once_with(uid='111753113@g.nccu.edu.tw')
    
            self.assertEqual(response.status_code, 200)
            self.assertEqual(json.loads(response.content), expected_response)


class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_register(self):
        with patch('JoDate.models.Users.objects.create') as mock_create:
            data = {
                'uid': '111753129@g.nccu.edu.tw',
                'username': 'May',
                'gender': 'F',
                'department': 'CS',
                'intro': 'Hello',
                'password': 'KK1234567',
            }
    
            json_data = json.dumps(data)

            request = self.factory.post('/register/', data=json_data, content_type='application/json')
            response = register(request)

            expected_result = JsonResponse({
                "User Info": {
                    "user ID": '111753129@g.nccu.edu.tw',
                    "user name": 'May',
                }
            })
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content, expected_result.content)


class ModifyUserViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_modify_user(self):
        with patch('JoDate.views.updateUser') as mock_update_user:
            mock_result = {'status': 'success'}
            mock_update_user.return_value = mock_result

            data = {
                'uid': '111753113@g.nccu.edu.tw',
                'username': 'Kevin',
                'intro': 'Nothing',
                'url': 'https://imgur.com/boT6QuE'
            }
            json_data = json.dumps(data)
            request = self.factory.post('/modifyuser/', data=json_data, content_type='application/json')

            response = modifyUser(request)

    
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content, JsonResponse(mock_result).content)

class ChangePasswordViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_change_password(self):
        # 使用 mock 來模擬 updatePassword 函式
        with patch('JoDate.views.updatePassword') as mock_update_password:
            mock_result = {'status': 'success'}
            mock_update_password.return_value = mock_result

            data = {
                'uid': '111753113@g.nccu.edu.tw',
                'origin_password': 'JJ1234567',
                'password': 'JJ7654321'
            }
            json_data = json.dumps(data)

            request = self.factory.post('/changepassword/', data=json_data, content_type='application/json')
            response = changePassword(request)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content, JsonResponse(mock_result).content)

class RemoveUserViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_remove_user(self):
        # 使用 mock 來模擬 deleteUser 函式
        with patch('JoDate.views.deleteUser') as mock_delete_user:

            mock_result = {'status': 'success'}
            mock_delete_user.return_value = mock_result

            data = {
                'uid': '111753113@g.nccu.edu.tw'
            }
            json_data = json.dumps(data)

            request = self.factory.post('/removeuser/', data=json_data, content_type='application/json')
            response = removeUser(request)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content, JsonResponse(mock_result).content)
       
class GetUserInfoViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_get_user_info(self):

        with patch('JoDate.views.getUser') as mock_get_user:
            mock_result = {'user_id': '111753113@g.nccu.edu.tw', 'username': 'Kevin'}
            mock_get_user.return_value = mock_result

            data = {
                'uid': '111753113@g.nccu.edu.tw'
            }
            json_data = json.dumps(data)
            request = self.factory.post('/getuserinfo/', data=json_data, content_type='application/json')
            response = getUserInfo(request)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content, JsonResponse(mock_result).content)

class GetUserGroupsViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_get_user_groups(self):
        with patch('JoDate.views.getAllUserGroups') as mock_get_all_user_groups:
            mock_result = {'groups': ['Group1', 'Group2']}
            mock_get_all_user_groups.return_value = mock_result

            data = {
                'uid': '111753113@g.nccu.edu.tw'
            }
            json_data = json.dumps(data)

            request = self.factory.post('/getusergroups/', data=json_data, content_type='application/json')
            response = getUserGroups(request)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content, JsonResponse(mock_result).content)

class GroupingViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_create_group(self):

        with patch('JoDate.views.createGroup') as mock_create_group:
            mock_result = {'status': 'success'}
            mock_create_group.return_value = mock_result

            data = {
                'group_name': 'Group1',
                'members': ['user1', 'user2']
            }
            json_data = json.dumps(data)

            request = self.factory.post('/creategroup/', data=json_data, content_type='application/json')

            response = grouping(request)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content, JsonResponse(mock_result).content)

class ModifyGroupViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_update_group(self):
        
        with patch('JoDate.views.updateGroup') as mock_update_group:
            mock_result = {'status': 'success'}
            mock_update_group.return_value = mock_result

            data = {
                'group_id': '12345',
                'group_name': 'Group1',
                'members': ['user1', 'user2']
            }
            json_data = json.dumps(data)

            request = self.factory.post('/updategroup/', data=json_data, content_type='application/json')
            response = modifyGroup(request)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content, JsonResponse(mock_result).content)

class ModifyAttendanceViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_update_attendance(self):

        with patch('JoDate.views.updateAttendance') as mock_update_attendance:
        
            mock_result = {'status': 'success'}
            mock_update_attendance.return_value = mock_result

            data = {
                'group_id': '12345',
                'attendance': 20
            }
            json_data = json.dumps(data)
            request = self.factory.post('/modifyattendence/', data=json_data, content_type='application/json')

            response = modifyAttendance(request)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content, JsonResponse(mock_result).content)

class GetGroupInfoViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_get_group_info(self):
        
        with patch('JoDate.views.getGroupbyID') as mock_get_group_by_id:
          
            mock_result = {'group_id': '12345', 'group_name': 'Group1'}
            mock_get_group_by_id.return_value = mock_result

            data = {
                'group_id': '12345'
            }
            json_data = json.dumps(data)
            request = self.factory.post('/getgroupinfo/', data=json_data, content_type='application/json')

            response = getGroupInfo(request)
           
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content, JsonResponse(mock_result).content)

class GetAllGroupsViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_get_all_groups(self):
        # 使用 mock 來模擬 getGroups 函式
        with patch('JoDate.views.getGroups') as mock_get_groups:
            # 模擬 getGroups 函式的回傳值
            mock_result = {'groups': ['Group1', 'Group2']}
            mock_get_groups.return_value = mock_result

            # 建立 POST request 的資料
            data = {
                'uid': '111753113@g.nccu.edu.tw'
            }
            json_data = json.dumps(data)

            request = self.factory.post('/getallgroups/', data=json_data, content_type='application/json')
            response = getAllGroups(request)


            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content, JsonResponse(mock_result).content)

class AttendanceTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_check_attendance(self):
       with patch('JoDate.views.getAttendanceStatus') as mock_get_attendance_status:
            # 模擬 getAttendanceStatus 方法回傳的結果
            mock_result = {'attended': True, 'isCreator': False}
            mock_get_attendance_status.return_value = mock_result

            data = {
                'user_id':  '111753113@g.nccu.edu.tw',
                'group_id': 1
            }

            json_data = json.dumps(data)

            request = self.factory.post('/checkattendence/', data=json_data, content_type='application/json')
            response = checkAttendance(request)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content, json.dumps(mock_result).encode('utf-8'))
class CheckGroupStatusViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_check_group_status(self):

        with patch('JoDate.views.updateGroupStatus') as mock_update_group_status:
    
            mock_result = [{'group_id': '12345', 'status': 'C'}, {'group_id': '67890', 'status': 'FA'}]
            mock_update_group_status.return_value = mock_result

            request = self.factory.post('/checkgroupstatus/')

            response = checkGroupStatus(request)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content, JsonResponse(mock_result, safe=False).content)
            mock_update_group_status.assert_called_once()
