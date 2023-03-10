from rest_framework import status
from rest_framework.test import APITestCase
from visionoflaborapi.models import User, Household, Chore
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
        chores = Chore.objects.all()
        chore = chores.filter(owner=user.id)
        user.chores = chore

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
        """Test whether a user updates on PUT at users/id
        """
        user = User.objects.first()
        if user.household is not None:
            updated_user = {
                "uid": user.uid,
                "first_name": f'{user.first_name} updated',
                "last_name": user.last_name,
                "household": user.household.id,
                "photo_url": user.photo_url,
                "admin": user.admin
            }
        else:
            updated_user = {
                "uid": user.uid,
                "first_name": f'{user.first_name} updated',
                "last_name": user.last_name,
                "household": None,
                "photo_url": user.photo_url,
                "admin": user.admin
            }



        url = f'/users/{user.id}'

        response = self.client.put(url, updated_user, format='json')

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        user.refresh_from_db()

        self.assertEqual(updated_user['first_name'], user.first_name)

    def test_change_user_if_household_is_null(self):
        """Test a change on a user if the user household is None
        """

        user = User.objects.filter(household__isnull=True).first()
        household = Household.objects.first()
        url = f'/users/{user.id}'

        updated_user = {
            "uid": user.uid,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "household": household.id,
            "photo_url": user.photo_url,
            "admin": user.admin
        }

        response = self.client.put(url, updated_user, format='json')

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        user.refresh_from_db()

        self.assertEqual(updated_user['household'], user.household.id)

    def test_destroy_user(self):
        """test DELETE user"""

        user = User.objects.first()

        url = f'/users/{user.id}'

        response = self.client.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
