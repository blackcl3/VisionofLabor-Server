from rest_framework.test import APITestCase
from visionoflaborapi.models import User

class AuthTests(APITestCase):

    fixtures = ['users', 'households']

    def setUp(self):

        self.user = User.objects.first()
        uid = self.user.uid
        self.client.credentials(HTTP_AUTHORIZATION=f"{uid}")

    def test_get_user(self):
        """test check_user method"""

        url = '/checkuser'

        uid = {
            "uid": self.user.uid
        }

        response = self.client.post(url, uid, format='json')

        expected = {
            'id': self.user.id,
            'uid': self.user.uid,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'full_name': self.user.full_name,
            'photo_url': self.user.photo_url,
            'household': {'id': self.user.household.id, 'name': self.user.household.name},
            'admin': self.user.admin,
        }

        self.assertEqual(expected, response.data)

    def test_get_user_with_no_household(self):
        """test check_user method if user has no household"""

        url = '/checkuser'

        users = User.objects.all()

        user = users.filter(household__isnull=True).first()

        uid = {
            "uid": user.uid
        }

        response = self.client.post(url, uid, format='json')

        expected = {
            'id': user.id,
            'uid': user.uid,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'full_name': user.full_name,
            'photo_url': user.photo_url,
            'household': None,
            'admin': user.admin,
        }

        self.assertEqual(expected, response.data)

    def test_check_user_bad_login_details(self):
        """test check user method with bad login details"""

        url = '/checkuser'

        uid = {
            "uid": 'null'
        }

        response = self.client.post(url, uid, format='json')

        expected = {'valid': False}

        self.assertEqual(expected, response.data)

    def test_register_user(self):
        """register user
        """

        url = '/register'

        user = {
            "uid": '6',
            "first_name": "Theodore",
            "last_name": " Twombly",
            "photo_url": "https://cdn.vox-cdn.com/thumbor/M8uk8NIvDNz1oFEw-CF9et2CA-U=/79x0:940x574/2050x1367/cdn.vox-cdn.com/assets/3729703/her_promotional_images29_1020.jpg",
            "admin": True
        }

        response = self.client.post(url, user, format='json')

        expected = {
            "id": response.data['id'],
            "uid": '6',
            "first_name": "Theodore",
            "last_name": " Twombly",
            "photo_url": "https://cdn.vox-cdn.com/thumbor/M8uk8NIvDNz1oFEw-CF9et2CA-U=/79x0:940x574/2050x1367/cdn.vox-cdn.com/assets/3729703/her_promotional_images29_1020.jpg",
            "admin": True
        }

        self.assertEqual(expected, response.data)
