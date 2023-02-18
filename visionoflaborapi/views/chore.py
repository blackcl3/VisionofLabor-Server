from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from visionoflaborapi.models import User, Household, Chore, ChoreCategory, Category


class ChoreViewSet(ViewSet):

    def retrieve(self, request, pk):
        """GET single chore"""
        chore = Chore.objects.get(pk=pk)
        chorecategories = ChoreCategory.objects.all()
        chore.category = chorecategories.filter(chore=chore.id)
        chore.category.update()

        serializer = ChoreSerializer(chore)
        return Response(serializer.data)

    def list(self, request):
        """GET all chores"""
        chores = Chore.objects.all()
        uid = request.query_params.get('uid', None)
        household_query = request.query_params.get('household', None)
        if uid is not None:
            user = User.objects.get(uid=uid)
            chores = chores.filter(owner=user)
        if household_query is not None:
            if household_query == 'empty':
                chores = chores.filter(household__isnull=True)
                serializer = ChoreSerializer(chores, many=True)
        serializer = ChoreSerializer(chores, many=True)
        return Response(serializer.data)

    def create(self, request):
        """POST for chore"""
        uid = request.META['HTTP_AUTHORIZATION']
        auth_user = User.objects.get(uid=uid)
        household = Household.objects.filter(id=request.data['household']).first()

        if auth_user.household.id is not household.id:
            return Response(None, status=status.HTTP_403_FORBIDDEN)
        categories = request.data['category']
        chore = Chore.objects.create(
            name=request.data['name'],
            description=request.data['description'],
            frequency=request.data['frequency'],
            priority=request.data['priority'],
            owner= User.objects.filter(pk=request.data['owner']).first(),
            photo_url=request.data['photo_url'],
            household=household
        )

        if categories is not None:
            for category in categories:
                category = ChoreCategory(chore=chore,
                                         category=Category.objects.get(pk=category["value"]))
                category.save()

        serializer = ChoreSerializer(chore)
        return Response(serializer.data)

    def update(self, request, pk):
        """PUT for chore

        Args:
            request (_type_): expecting PUT request with JSON object for payload
            pk (_type_): expecting PK for chore item

        Returns:
            204 response if successful
        """
        #check if user exists in household; if not, don't allow them to edit
        uid = request.META['HTTP_AUTHORIZATION']
        auth_user = User.objects.get(uid=uid)
        chore = Chore.objects.get(pk=pk)
        household = Household.objects.filter(
            pk=chore.household.id).first()
        if auth_user.household.id is not household.id:
            return Response(None, status=status.HTTP_403_FORBIDDEN)

        chore = Chore.objects.get(pk=pk)
        categories = request.data['category']
        chore.name = request.data['name']
        chore.description = request.data['description']
        chore.frequency = request.data['frequency']
        chore.priority = request.data['priority']
        chore.owner = User.objects.filter(pk=request.data['owner']).first()
        chore.photo_url = request.data['photo_url']
        chore.household = household

        chore_categories = list(ChoreCategory.objects.filter(chore=chore))

        if chore_categories is not None:
            for category in chore_categories:
                category.delete()

        if categories is not None:
            for category in categories:
                chore_category = ChoreCategory(chore=chore,
                                               category=Category.objects.get(pk=category['value']))
                chore_category.save()

        chore.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self,request, pk):
        """DELETE chore"""
        # check if user exists in household; if not, don't allow them to delete
        uid = request.META['HTTP_AUTHORIZATION']
        auth_user = User.objects.get(uid=uid)
        chore = Chore.objects.get(pk=pk)
        household = Household.objects.filter(
            pk=chore.household.id).first()
        if auth_user.household.id is not household.id:
            return Response(None, status=status.HTTP_403_FORBIDDEN)
        chore.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


    @action(methods=['put'], detail=True)
    def clone_chore(self, request, pk):
        """Clones sample chore"""
        user = User.objects.get(uid=request.data['uid'])
        if user.household is not None:
            chore = Chore.objects.get(pk=pk)
            chore.pk = None
            chore.household = user.household
            chore.save()
            return Response(None, status=status.HTTP_200_OK)
        else:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

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
        depth = 1
