from django.test import TestCase
from django.utils import timezone
from JoDate.models import *

from django.test import TestCase
from .models import Users, Group

class ModelsIntegrationTest(TestCase):

    def setUp(self):
        self.user = Users.objects.create(
            uid='1@g.nccu.edu.tw',
            name='John Doe',
            password='123456',
            gender='M',
            department='Computer Science',
            credit=100,
            self_intro='Hello, I am John Doe.',
            url='https://imgur.com/ITSlWZA'
        )
        self.group = Group.objects.create(
            creator='1@g.nccu.edu.tw',
            title='Party',
            type='A',
            location='Central Park',
            info='Join us for a fun party!',
            min_require=2,
            max_require=20,
            actual=0,
            status='A'
        )
        self.group.User.add(self.user)

    def test_users_model(self):
        # 測試Users模型
        self.assertEqual(self.user.uid, '1@g.nccu.edu.tw')
        self.assertEqual(self.user.name, 'John Doe')
        self.assertEqual(self.user.password, '123456')
        self.assertEqual(self.user.gender, 'M')
        self.assertEqual(self.user.department, 'Computer Science')
        self.assertEqual(self.user.credit, 100)
        self.assertEqual(self.user.self_intro, 'Hello, I am John Doe.')
        self.assertEqual(self.user.url, 'https://imgur.com/ITSlWZA')

    def test_group_model(self):
        # 測試Group模型
        self.assertEqual(self.group.creator, '1@g.nccu.edu.tw')
        self.assertEqual(self.group.title, 'Party')
        self.assertEqual(self.group.type, 'A')
        self.assertEqual(self.group.location, 'Central Park')
        self.assertEqual(self.group.info, 'Join us for a fun party!')
        self.assertEqual(self.group.min_require, 2)
        self.assertEqual(self.group.max_require, 20)
        self.assertEqual(self.group.actual, 0)
        self.assertEqual(self.group.status, 'A')
        self.assertEqual(self.group.User.count(), 1)
        self.assertIn(self.user, self.group.User.all())
