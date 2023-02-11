from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from visionoflaborapi.models import User, Household, Chore, ChoreCategory

class HouseholdViewSet(ViewSet):

    def retrieve(self, request, pk):
        """GET request for a single household"""

        household = Household.objects.get(pk=pk)
        users = User.objects.all()
        chores = Chore.objects.all()
        chorecategories = ChoreCategory.objects.all()
        household.users = users.filter(household=pk)
        household.users.update()
        household.chores = chores.filter(household=pk)
        household.chores.update()
        for chore in household.chores:
            chore.category = chorecategories.filter(chore=chore.id)
            chore.category.update()
            

        serializer = HouseholdSerializer(household)
        return Response(serializer.data)

class ChoreCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChoreCategory
        fields = ('id', 'category')
        depth = 1

class ChoreSerializer(serializers.ModelSerializer):
    category = ChoreCategorySerializer(many=True, read_only=True)
    class Meta:
        model = Chore
        fields = ('id', 'name', 'description',
                  'frequency', 'priority', 'owner', 'photo_url', 'household', 'category')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'uid', 'first_name', 'last_name',
                  'full_name', 'household', 'photo_url', 'admin')

class HouseholdSerializer(serializers.ModelSerializer):
    chores = ChoreSerializer(many=True, read_only=True)
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Household
        fields = ('id', 'name', 'users', 'chores')
