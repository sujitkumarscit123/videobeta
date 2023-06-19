from django.utils.encoding import force_bytes
from gitdb.utils.encoding import force_text
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .models import User, Role, UserRole


@api_view(['POST'])
def signup(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if User.objects.filter(username=username).exists():
        return Response({'message': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)
    role = Role.objects.get(name='User')  # Get the 'User' role
    user = User.objects.create_user(username=username, password=password)
    UserRole.objects.create(user=user, role=role)  # Assign the 'User' role to the user

    return Response({'message': 'User created successfully.'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    role = request.data.get('role')

    user = authenticate(request._request, username=username, password=password)
    if user is not None and user.roles.filter(name=role).exists():
        request.session['user_id'] = user.pk
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        return Response({'token': token, 'uid': uid}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Invalid credentials or role.'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def validate_token(request):
    token = request.data.get('token')
    uid = request.data.get('uid')

    try:
        uid = force_text(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        return Response({'message': 'Valid token.'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def reset_password(request):
    username = request.data.get('username')
    password = request.data.get('password')

    admin_role = Role.objects.get(name='Admin')
    if not request.user.roles.filter(pk=admin_role.pk).exists():
        return Response({'message': 'Unauthorized.'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'message': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    user.set_password(password)
    user.save()

    return Response({'message': 'Password reset successfully.'}, status=status.HTTP_200_OK)