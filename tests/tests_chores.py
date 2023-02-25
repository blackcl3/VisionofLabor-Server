from rest_framework import status
from rest_framework.test import APITestCase
from visionoflaborapi.models import User, Chore, ChoreCategory
from visionoflaborapi.views.chore import ChoreSerializer

class ChoreTests(APITestCase):

    fixtures = ['users', 'households', 'chores', 'chorecategories', 'categories']

    def setUp(self):

        self.user = User.objects.first()
        uid = self.user.uid
        self.client.credentials(HTTP_AUTHORIZATION=f"{uid}")

    def test_get_chore(self):
        """tests getting an individual chore
        """
        chore = Chore.objects.first()
        chorecategories = ChoreCategory.objects.all()
        categories = chorecategories.filter(chore=chore)
        chore.category = categories

        url = f'/chores/{chore.id}'

        response = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        expected = ChoreSerializer(chore)

        self.assertEqual(expected.data, response.data)

    def test_get_all_chores(self):
        """tests getting all chores
        """

        url = '/chores'

        response = self.client.get(url)

        chores = Chore.objects.all()

        expected = ChoreSerializer(chores, many=True)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected.data, response.data)

    def test_create_chore(self):
        """test for creating a chore"""
        url = '/chores'

        user = User.objects.first()

        chore = {
            "name": "wash card",
            "description": "washing the car",
            "frequency": "monthly",
            "priority": "not necessary",
            "owner": user.id,
            "photo_url": "https://media.wired.com/photos/6385715a402153462d49763e/4:3/w_1745,h_1308,c_limit/Volvo-EX90-Featured-Gear.jpg",
            "household": user.household.id,
            "category": [],
        }

        response = self.client.post(
            url, chore, format='json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        new_chore = Chore.objects.last()

        expected = ChoreSerializer(new_chore)

        self.assertEqual(expected.data, response.data)

    def test_delete_chore(self):
        """test DELETE chore"""

        chore = Chore.objects.first()

        url = f'/chores/{chore.id}'

        response = self.client.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
