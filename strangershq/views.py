from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework import status
from . import database, pfp_tracking, leader_board
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from .serializers import AddUserSerializer, ReturnUserSerializer, UpdateHometownSerializer, UpdateInterestsSerializer, TwitterTrackingSerializer, LeaderboardSerializer


def home(request):
    return render(request, 'home.html')

class AddUserView(APIView):
    @swagger_auto_schema(
        request_body=AddUserSerializer,
        operation_id='add_user'
    )
    def post(self, request):
        serializer = AddUserSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            print("-------")
            print(validated_data)
            print("-------")
            # Process the validated data
            address = validated_data['address']
            twitter_id = validated_data['twitter_id']
            token_id = validated_data['token_id']
            twitter_url = validated_data['twitter_url']
            hometown = validated_data['hometown']
            disc_handle = validated_data['disc_handle']
            interests = validated_data['interests']
            # Perform further processing with the data
            result = database.dbAddUser(address, twitter_id, token_id, twitter_url, hometown, disc_handle, interests)
            # print("------")
            # print(result)
            # print("------")
            return Response({'message': f'{result}'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ReturnUserView(APIView):
    @swagger_auto_schema(request_body=ReturnUserSerializer, operation_id='return_user')
    def post(self, request):
        serializer = ReturnUserSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            # Process the validated data
            address = validated_data['address']
            result = database.dbQueryRow(address)
            print(result)
            return Response({'message': result})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class DeleteUserView(APIView):
    @swagger_auto_schema(request_body=ReturnUserSerializer, operation_id='delete_user')
    def post(self, request):
        serializer = ReturnUserSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            # Process the validated data
            address = validated_data['address']
            result = database.dbDeleteRow(address)
            if result['status'] == 'Success':
                return Response({'message': f'{address} deleted successfully'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class UpdateUserHometownView(APIView):
    @swagger_auto_schema(request_body=UpdateHometownSerializer, operation_id='update_user_hometown')
    def post(self, request):
        serializer = UpdateHometownSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            # Process the validated data
            address = validated_data['address']
            hometown = validated_data['hometown']
            result = database.dbUpdateHometown(address, hometown)
            if result['status'] == 'Success':
                return Response({'message': f'{address} successfully changed hometown to: {hometown}'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateUserInterestsView(APIView):
    @swagger_auto_schema(request_body=UpdateInterestsSerializer, operation_id='update_user_interests')
    def post(self, request):
        serializer = UpdateInterestsSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            # Process the validated data
            address = validated_data['address']
            interests = validated_data['interests']
            result = database.dbUpdateInterests(address, interests)
            if result['status'] == 'Success':
                return Response({'message': f'{address} successfully changed interests to: {interests}'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                               
class LeaderboardView(APIView):
    @swagger_auto_schema(request_body=LeaderboardSerializer, operation_id='leaderboard_info')
    def post(self, request):
        serializer = LeaderboardSerializer(data=request.data)
        if serializer.is_valid():
            # Process the validated data
            result = leader_board.leaderBoardReturn()
            return Response({'message': result})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TwitterTrackingView(APIView):
    @swagger_auto_schema(request_body=TwitterTrackingSerializer, operation_id='pfp_compare')
    def post(self, request):
        serializer = TwitterTrackingSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            # Process the validated data
            token_id = validated_data['token_id']
            twitter_url = validated_data['handle']
            result = pfp_tracking.twitterTracking(token_id, twitter_url)
            return Response({'message': result})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

