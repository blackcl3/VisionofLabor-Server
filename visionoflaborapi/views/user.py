from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from visionoflaborapi.models import User, Household

class UserViewSet(ViewSet):

    def retrieve(self, request, pk):
        """GET requests for a single user

        Args:
            response -- JSON serialized user
        """
        user = User.objects.get(pk=pk)

        serializer = UserSerializer(user)
        return Response(serializer.data)

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
        household = Household.objects.get(pk=request.data['household'])

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

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'uid', 'first_name', 'last_name',
                  'full_name', 'household', 'photo_url', 'admin')
        depth=1
