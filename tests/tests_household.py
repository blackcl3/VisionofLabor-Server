from rest_framework import status
from rest_framework.test import APITestCase
from visionoflaborapi.models import User, Household, Chore
from visionoflaborapi.views.household import HouseholdSerializer

class HouseholdTests(APITestCase):

    fixtures = ['users', 'households']

    def setUp(self):

        self.user = User.objects.first()
        uid = User.objects.get(uid=self.user.uid)
        self.client.credentials(HTTP_AUTHORIZATION=f"{uid}")

    def test_get_household(self):
        """tests GET for a single household
        """

        household = Household.objects.first()
        users = User.objects.filter(household=household)
        chores = Chore.objects.filter(household=household.id)
        household.users = users
        household.chores = chores

        url = f'/household/{household.id}'

        response = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        expected = HouseholdSerializer(household)

        self.assertEqual(expected.data, response.data)

    def test_get_all_households(self):
        """testing GET for all households
        """

        url = '/household'

        response = self.client.get(url)

        households = Household.objects.all()

        expected = HouseholdSerializer(households, many=True)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected.data, response.data)

    def test_create_household(self):
        """test for creating a household
        """

        url = '/household'
        user = User.objects.last()

        household = {
            "uid": user.uid,
            "name": "Twin Peaks Sheriff's Department",
            "users":[{"value": user.id}],
        }

        response = self.client.post(url, household, format='json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        new_household = Household.objects.last()

        expected = HouseholdSerializer(new_household)

        self.assertEqual(expected.data, response.data)

    def test_create_household_errors_if_user_has_household(self):
        """test to make sure an error is thrown if a user

        tries to create a household and is already associated with a household
        """
        url = '/household'

        user = User.objects.filter(household__isnull=False).first()

        household = {
            "uid": user.uid,
            "name": "Twin Peaks Sheriff's Department",
            "users": [{"value": user.id}],
        }

        response = self.client.post(url, household, format='json')

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_change_household(self):
        """test whether a household updates on PUT"""

        household = Household.objects.first()
        users = User.objects.filter(household=household).first()

        updated_household = {
            "name": f'{household.name} updated',
            "users": [{"value": users.id}]
        }

        url = f'/household/{household.id}'

        response = self.client.put(url, updated_household, format='json')

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        household.refresh_from_db()

        self.assertEqual(updated_household['name'], household.name)
