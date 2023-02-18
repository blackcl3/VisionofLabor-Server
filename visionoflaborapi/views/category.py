from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from visionoflaborapi.models import Category

class CategoryViewSet(ViewSet):

    def list(self, request):
        """GET all categories"""

        categories = Category.objects.all()

        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('value', 'label')
