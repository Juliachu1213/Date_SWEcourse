from django.test import TestCase
from JoDate.menu import *

from django.test import TestCase
from unittest.mock import patch
from django.core.exceptions import ObjectDoesNotExist

class GetUserTestCase(TestCase):
    def setUp(self):
        # 在測試中使用的假資料
        self.fake_user_info = {
            'uid': '111753113@g.nccu.edu.tw'
        }
        self.fake_invalid_info = {
            'uid': None
        }
        self.fake_nonexistent_info = {
            'uid': 'xyz'
        }
        self.fake_user_data = {
            'uid': '111753113@g.nccu.edu.tw',
            'name': 'John Doe'
        }

    @patch('JoDate.models.Users.objects')
    def test_get_user_valid_uid(self, mock_users_objects):
        # 假設 Users.objects.filter 返回假資料
        mock_users_objects.filter.return_value.values.return_value = [self.fake_user_data]

        result = getUser(self.fake_user_info)

        # 檢查結果是否符合預期
        expected_result = {'user': [self.fake_user_data]}
        self.assertEqual(result, expected_result)

    def test_get_user_invalid_uid(self):
        result = getUser(self.fake_invalid_info)

        # 檢查結果是否符合預期
        expected_result = {'Error': 'Invalid ID input'}
        self.assertEqual(result, expected_result)


class GetGroupByIDTestCase(TestCase):
    def setUp(self):
        # 在測試中使用的假資料
        self.fake_group_info = {
            'gid': '123'
        }
        self.fake_invalid_info = {
            'gid': None
        }
        self.fake_nonexistent_info = {
            'gid': ''
        }
        self.fake_group_data = {
            'id': '123',
            'name': 'Group A'
        }
        self.fake_user_data = {
            'uid': '111000006',
            'name': '王小明'
        }

    @patch('JoDate.models.Group.objects')
    def test_get_group_by_id_valid_gid(self, mock_group_objects):
        # 假設 Group.objects.filter 返回假資料
        mock_group_objects.filter.return_value.values.return_value = [self.fake_group_data]
        # 假設 Group.objects.get 返回假資料
        mock_group_objects.get.return_value.User.all.return_value = [Users(**self.fake_user_data)]

        result = getGroupbyID(self.fake_group_info)

        # 檢查結果是否符合預期
        expected_result = {'Group': [self.fake_group_data], 'Group Attendance': ['111000006 王小明']}
        self.assertEqual(result, expected_result)

    def test_get_group_by_id_invalid_gid(self):
        result = getGroupbyID(self.fake_invalid_info)

        # 檢查結果是否符合預期
        expected_result = {'Error': 'Invalid ID input'}
        self.assertEqual(result, expected_result)

    @patch('JoDate.models.Group.objects')
    def test_get_group_by_id_nonexistent_gid(self, mock_group_objects):
        # 假設 Group.objects.filter 沒有找到匹配的資料，拋出 ObjectDoesNotExist 異常
        mock_group_objects.filter.side_effect = ObjectDoesNotExist

        result = getGroupbyID(self.fake_nonexistent_info)

        # 檢查結果是否符合預期
        expected_result = {'Error': 'group ID does not exist'}
        self.assertEqual(result, expected_result)
