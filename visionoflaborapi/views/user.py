from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
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
        if uid is not None:
            users = users.filter(uid=uid)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'uid', 'first_name', 'last_name',
                  'full_name', 'household', 'photo_url', 'admin')
        depth=1
