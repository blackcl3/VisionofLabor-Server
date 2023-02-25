from rest_framework import status
from rest_framework.test import APITestCase
from visionoflaborapi.models import User, Category, Household
from visionoflaborapi.views.category import CategorySerializer

class CategoryTests(APITestCase):
    
    fixtures = ['users', 'categories', 'households']
    
    def setUp(self):
        
        self.user = User.objects.first()
        uid = self.user.uid
        self.client.credentials(HTTP_AUTHORIZATION=f"{uid}")
        
    def test_get_all_categories(self):
        """tests getting all categories
        """
        
        url = '/categories'
        
        response = self.client.get(url)
        
        categories = Category.objects.all()
        
        expected = CategorySerializer(categories, many=True)
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected.data, response.data)
        
