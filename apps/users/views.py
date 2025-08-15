from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.models import User
# Create your views here.
@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user':serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST','GET'])
def login_user(request):
 username = request.data.get('username')
 password = request.data.get('password')
 user = authenticate(username=username, password=password)
 if user is not None:
     refresh = RefreshToken.for_user(user)
     serializer = UserSerializer(user)
     return Response({
         'refresh': str(refresh),
         'access': str(refresh.access_token),
         'user':serializer.data}, status=status.HTTP_200_OK)
 return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
@api_view(['GET'])
def get_all_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
# @api_view(['GET','PUT'])
# def manage_user_details(request,user_id):
#    user = User.objects.get(id=user_id)
#    if request.method =="GET":
#        serializer = UserSerializer(user)
#        return Response(serializer.data)
#    elif request.method == "PUT":
#        serializer = UserSerializer(user, data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def AddprofileDetails(request):
   if request.method == 'POST':
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = ProfileSerializer(profile,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_user_credentials(request):
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    if not user.check_password(old_password):
        return Response({'error': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
    serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():    
     user.set_password(new_password)
     user.save()
    return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
