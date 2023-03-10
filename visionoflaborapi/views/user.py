from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from visionoflaborapi.models import User, Household, Chore

class UserViewSet(ViewSet):

    def retrieve(self, request, pk):
        """GET requests for a single user

        Args:
            response -- JSON serialized user
        """
        try:
            user = User.objects.get(pk=pk)
            chores = Chore.objects.all()
            user.chores = chores.filter(owner=user.id)
            user.chores.update()
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """GET request for all users"""

        users = User.objects.all()
        uid = request.query_params.get('uid', None)
        household_query = request.query_params.get('household', None)
        if uid is not None:
            users = users.filter(uid=uid)
        if household_query is not None:
            if household_query == 'empty':
                users = users.filter(household__isnull=True)
                serializer = UserSerializer(users, many=True)
                return Response(serializer.data)
            else:
                user_household = Household.objects.get(pk=household_query)
                users = users.filter(household=user_household.id)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def update(self, request, pk):
        """PUT for user"""
        user = User.objects.get(pk=pk)
        uid = request.query_params.get('uid', None)
        if uid is not None:
            user = User.objects.get(uid=uid)
        household = Household.objects.filter(pk=request.data['household']).first()

        user.first_name = request.data['first_name']
        user.last_name = request.data['last_name']
        user.household = household
        user.photo_url = request.data['photo_url']
        user.admin = request.data['admin']
        user.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """DELETE user"""

        user = User.objects.get(pk=pk)
        user.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class ChoreSerializer(serializers.ModelSerializer):
     
     class Meta:
         model = Chore
         fields = ('id', 'name', 'description',
                   'frequency', 'priority', 'owner', 'photo_url', 'household', 'status')

class UserSerializer(serializers.ModelSerializer):
    chores = ChoreSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ('id', 'uid', 'first_name', 'last_name',
                  'full_name', 'household', 'photo_url', 'admin', 'chores')
        depth=1
