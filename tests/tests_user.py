from rest_framework import status
from rest_framework.test import APITestCase
from visionoflaborapi.models import User, Household
from visionoflaborapi.views.user import UserSerializer

class UserTests(APITestCase):

    fixtures = ['users', 'households']

    def setUp(self):

        self.user = User.objects.first()
        uid = User.objects.get(uid=self.user.uid)
        self.client.credentials(HTTP_AUTHORIZATION=f"{uid}")

    def test_get_user(self):
        """Test to get a single user
        """
        user = User.objects.first()

        url = f'/users/{user.id}'

        response = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        expected = UserSerializer(user)

        self.assertEqual(expected.data, response.data)

    def test_get_all_users(self):
        """Test to get all users
        """
        url = '/users'

        response = self.client.get(url)

        users = User.objects.all()

        expected = UserSerializer(users, many=True)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected.data, response.data)

    def test_change_user(self):

        user = User.objects.first()

        url = f'/users/{user.id}'

        updated_user = {
            "uid": user.uid,
            "first_name": f'{user.first_name} updated',
            "last_name": user.last_name,
            "household": user.household.id,
            "photo_url": user.photo_url,
            "admin": user.admin
        }

        response = self.client.put(url, updated_user, format='json')

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        user.refresh_from_db()

        self.assertEqual(updated_user['first_name'], user.first_name)
