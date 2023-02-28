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

    def list(self, request):
        """GET request for All Households"""
        household = Household.objects.all()

        serializer = HouseholdSerializer(household, many=True)
        return Response(serializer.data)

    def create(self, request):
        """POST for household

        Pass in JSON object
        Can pass in Users to be associated with given household
        """

        household_users = request.data['users']
        user = User.objects.get(uid=request.data['uid'])
        if user.household is not None:
            return Response(None, status=status.HTTP_403_FORBIDDEN)

        household = Household.objects.create(
            name=request.data['name']
        )
        user.household = household
        user.save()

        if household_users is not None:
            for user in household_users:
                user = User.objects.get(pk=user['value'])
                user.household = household
                user.save(update_fields=['household'])
        serializer = HouseholdSerializer(household)
        return Response(serializer.data)


    def update(self, request, pk):
        """PUT for household"""

        household = Household.objects.get(pk=pk)
        household_users = request.data['users']

        household.name = request.data['name']

        if household_users is not None:
            household_user = User.objects.all()
            household_user = User.objects.filter(household=household)
            for user in household_user:
                user.household = None
                user.save()

        if household_users is not None:
            for user in household_users:
                user = User.objects.get(pk=user['value'])
                user.household = household
                user.save(update_fields=['household'])

        household.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


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
                  'frequency', 'priority', 'owner', 'photo_url', 'household', 'category', 'status')
        depth = 1


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
