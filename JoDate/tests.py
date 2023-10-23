from django.test import TestCase
from JoDate.models import Users,Group

# Create your tests here.
class UserTestCase(TestCase):
    def setUp(self):
        Users.objects.create(
            uid="111306001",name="杜甫",password="12345678",
            gender="M", department="資訊管理學系", self_intro="略..."
        )

    def test_Users_info(self):
        user1 = Users.objects.get(uid="111306001")
        print(user1.get_gender_display())
        self.assertEqual(user1.get_gender_display(), 'Male')
