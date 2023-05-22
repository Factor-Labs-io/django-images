from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework import generics, status
from . import database, pfp_tracking, leader_board
from .models import User
import json
from drf_yasg import openapi
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from .serializers import AddUserSerializer, ReturnUserSerializer, UpdateHometownSerializer, UpdateInterestsSerializer, TwitterTrackingSerializer, LeaderboardSerializer, ReturnAllSerializer
import requests

class HealthCheckView(APIView):
    @swagger_auto_schema(operation_description="Health Check endpoint.")
    def get(self, request):
        return Response({"status": "Server is working"})

class ConsumeAPI(APIView):
    @swagger_auto_schema(
        operation_id='add_user',
        manual_parameters=[
            openapi.Parameter('token_id', openapi.IN_PATH, type=openapi.TYPE_STRING),
            openapi.Parameter('handle', openapi.IN_PATH, type=openapi.TYPE_STRING),
        ]
    )
    def get(self, request, token_id, handle):

        url = "https://0n1-test.factorlabs.io/v1/pfptracking"
        headers = {
            "Content-Type": "application/json",
            # If the endpoint requires authentication, you need to provide it here
            # "Authorization": "Bearer your_token",
        }
        data = {
            "token_id": token_id,
            "handle": handle
        }
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            return Response(response.json(), status=status.HTTP_200_OK)
        else:
            return Response(response.json(), status=status.HTTP_400_BAD_REQUEST)
        
def home(request):
    return render(request, 'home.html')

class AddUserView(APIView):
    @swagger_auto_schema(request_body=AddUserSerializer, operation_id='add_user')
    def post(self, request):
        data = request.data
    
        user = User.objects.create(
            address=data.get('address'),
            twitter_id=data.get('twitter_id'),
            token_id=data.get('token_id'),
            twitter_pfp_url=data.get('twitter_url'),
            hometown=data.get('hometown'),
            discord_handle=data.get('disc_handle'),
            interests=data.get('interests')
        )
    
        # Return a JSON response indicating success
        return JsonResponse({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

class ReturnUserView(generics.ListAPIView):
    serializer_class = ReturnAllSerializer

    @swagger_auto_schema(manual_parameters=[openapi.Parameter('address', openapi.IN_PATH, type=openapi.TYPE_STRING)], operation_id='return_user')
    def get(self, request, *args, **kwargs):
        address = self.kwargs.get('address')

        try:
            # Retrieve the user based on the given address
            user = User.objects.get(address=address)

            # Process the retrieved user data
            serialized_user = self.serializer_class(user)

            # Return the serialized user data
            return Response(serialized_user.data)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)

class DeleteUserView(generics.DestroyAPIView):
    serializer_class = ReturnAllSerializer

    @swagger_auto_schema(manual_parameters=[openapi.Parameter('address', openapi.IN_PATH, type=openapi.TYPE_STRING)], operation_id='delete_user')
    def delete(self, request, *args, **kwargs):
        address = self.kwargs.get('address')

        try:
            # Retrieve the user based on the given address
            user = User.objects.get(address=address)

            # Delete the user from the database
            user.delete()

            return Response({'message': 'User deleted successfully'})
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)

class UpdateUserHometownView(APIView):
    @swagger_auto_schema(
        request_body=UpdateHometownSerializer,
        operation_id='update_user_hometown',
    )
    def put(self, request):
        serializer = UpdateHometownSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            # Process the validated data
            address = validated_data['address']
            hometown = validated_data['hometown']
            try:
                user = User.objects.get(address=address)
                user.hometown = hometown
                user.save()
                return Response(
                    {
                        'message': f'{address} successfully changed interests to: {hometown}'
                    }
                )
            except User.DoesNotExist:
                return Response(
                    {'error': f'User with address {address} does not exist'},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)       
# class UpdateUserHometownView(APIView):
#     @swagger_auto_schema(request_body=UpdateHometownSerializer, operation_id='update_user_hometown')
#     def post(self, request):
#         serializer = UpdateHometownSerializer(data=request.data)
#         if serializer.is_valid():
#             validated_data = serializer.validated_data
#             # Process the validated data
#             address = validated_data['address']
#             hometown = validated_data['hometown']
#             result = database.dbUpdateHometown(address, hometown)
#             if result['status'] == 'Success':
#                 return Response({'message': f'{address} successfully changed hometown to: {hometown}'})
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateUserInterestsView(APIView):
    @swagger_auto_schema(
        request_body=UpdateInterestsSerializer,
        operation_id='update_user_interests',
    )
    def put(self, request):
        serializer = UpdateInterestsSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            # Process the validated data
            address = validated_data['address']
            interests = validated_data['interests']
            try:
                user = User.objects.get(address=address)
                user.interests = interests
                user.save()
                return Response(
                    {
                        'message': f'{address} successfully changed interests to: {interests}'
                    }
                )
            except User.DoesNotExist:
                return Response(
                    {'error': f'User with address {address} does not exist'},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                               
class LeaderboardView(APIView):
    @swagger_auto_schema(manual_parameters=[openapi.Parameter('parameter_name', openapi.IN_QUERY, type=openapi.TYPE_STRING)], operation_id='leaderboard_info')
    def get(self, request):
        serializer = LeaderboardSerializer(data=request.query_params)
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
        
# class QueryAllView(generics.RetrieveAPIView):
#     serializer_class = ReturnAllSerializer

#     def get(self, request, *args, **kwargs):

#         try:
#             # Process the retrieved user data
#             result = database.dbQueryAll()
#             return Response({'message': result})
#         except User.DoesNotExist:
#             return Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)

class QueryAllView(generics.ListAPIView):
    serializer_class = ReturnAllSerializer

    def get(self, request, *args, **kwargs):
        try:
            # Process the retrieved user data
            queryset = User.objects.all()
            user_instances = list(queryset)
            user_serialized = self.serializer_class(user_instances, many=True).data

            # Convert the serialized data to normal JSON format
            formatted_json = json.dumps(user_serialized)

            # Return the JSON response
            return HttpResponse(formatted_json, content_type='application/json')
        except User.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)


        

