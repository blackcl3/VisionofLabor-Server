from rest_framework.decorators import api_view
from rest_framework.response import Response
from visionoflaborapi.models import User, Household

@api_view(['POST'])
def check_user(request):
    '''Checks to see if User has Associated User

    Method arguments:
      request -- The full HTTP request object
    '''
    uid = request.data['uid']
    # Use the built-in authenticate method to verify
    # authenticate returns the user object or None if no user is found
    user = User.objects.filter(uid=uid).first()

    if user is not None:
        if user.household is not None:
            household = Household.objects.filter(
                id=user.household.id).first()
            data = {
                'id': user.id,
                'uid': user.uid,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'full_name': user.full_name,
                'photo_url': user.photo_url,
                'household': {'id': household.id, 'name': household.name},
                'admin': user.admin,

            }
        else:
            data = {
                'id': user.id,
                'uid': user.uid,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'full_name': user.full_name,
                'photo_url': user.photo_url,
                'household': None,
                'admin': user.admin,

            }
        return Response(data)
    # If authentication was successful, respond with their token
    else:
        # Bad login details were provided. So we can't log the user in.
        data = {'valid': False}
        return Response(data)


@api_view(['POST'])
def register_user(request):
    '''Handles the creation of a new user for authentication

    Method arguments:
      request -- The full HTTP request object
    '''

    # Now save the user info in the commonmealapi_user table
    user = User.objects.create(
        uid=request.data['uid'],
        first_name=request.data['first_name'],
        last_name=request.data['last_name'],
        photo_url=request.data['photo_url'],
        admin = request.data['admin'],
    )

    # Return the user info to the client
    data = {
        'id': user.id,
        'uid': user.uid,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'photo_url': user.photo_url,
        'admin': user.admin
    }
    return Response(data)
